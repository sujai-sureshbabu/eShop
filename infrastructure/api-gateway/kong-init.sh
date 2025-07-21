#!/bin/bash
set -xe
echo "Starting Kong init script..."

KONG_ADMIN_URL="http://kong:8001"

echo "Waiting for Kong Admin API..."
until curl -s "$KONG_ADMIN_URL/status" | grep -q '"reachable":true'; do
  echo "Kong Admin API not ready yet. Sleeping 3s..."
  sleep 3
done

echo "Kong Admin API ready. Starting configuration..."

echo "Registering services..."
jq -c '.services[]' /kong-services.json | while read -r service; do
  name=$(echo "$service" | jq -r '.name')
  url=$(echo "$service" | jq -r '.url')

  # Create or update service
  existing_service=$(curl -s "$KONG_ADMIN_URL/services/$name" || echo "{}")
  service_id=$(echo "$existing_service" | jq -r '.id // empty')

  if [ -z "$service_id" ]; then
    echo "Creating service $name"
    curl -s -X POST "$KONG_ADMIN_URL/services" \
      --data name="$name" \
      --data url="$url" | jq
  else
    echo "Service $name exists. Updating URL."
    curl -s -X PATCH "$KONG_ADMIN_URL/services/$name" \
      --data url="$url" | jq
  fi

  # Create/update routes for the service
  echo "$service" | jq -c '.routes[]' | while read -r route; do
    route_name=$(echo "$route" | jq -r '.name')

    echo "$route" | jq -r '.paths[]' | while read -r path; do
      existing_route=$(curl -s "$KONG_ADMIN_URL/services/$name/routes/$route_name" || echo "{}")
      route_id=$(echo "$existing_route" | jq -r '.id // empty')

      if [ -z "$route_id" ]; then
        echo "Creating route $route_name for service $name with path $path"
        curl -s -X POST "$KONG_ADMIN_URL/services/$name/routes" \
          --data name="$route_name" \
          --data "paths[]=$path" | jq
      else
        echo "Route $route_name exists. Updating path $path."
        curl -s -X PATCH "$KONG_ADMIN_URL/services/$name/routes/$route_name" \
          --data "paths[]=$path" | jq
      fi
    done
  done
done 

echo "Kong configuration complete."
