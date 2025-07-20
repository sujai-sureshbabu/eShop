#!/bin/bash
set -e

KONG_ADMIN_URL="http://kong:8001"

# Wait for Kong Admin API to be ready
echo "Waiting for Kong Admin API..."
until curl -s "$KONG_ADMIN_URL/status" | grep -q '"database":"running"'; do
  echo "Kong Admin API not ready yet. Sleeping 3s..."
  sleep 3
done

echo "Kong Admin API is ready. Configuring services and routes..."

create_or_update_service() {
  local name=$1
  local url=$2

  service=$(curl -s "$KONG_ADMIN_URL/services/$name" || echo "{}")
  service_id=$(echo "$service" | jq -r '.id // empty')

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
}

create_or_update_route() {
  local service_name=$1
  local route_name=$2
  local paths=$3

  route=$(curl -s "$KONG_ADMIN_URL/services/$service_name/routes/$route_name" || echo "{}")
  route_id=$(echo "$route" | jq -r '.id // empty')

  if [ -z "$route_id" ]; then
    echo "Creating route $route_name for service $service_name"
    curl -s -X POST "$KONG_ADMIN_URL/services/$service_name/routes" \
      --data name="$route_name" \
      --data "paths[]=$paths" | jq
  else
    echo "Route $route_name exists. Updating paths."
    curl -s -X PATCH "$KONG_ADMIN_URL/services/$service_name/routes/$route_name" \
      --data "paths[]=$paths" | jq
  fi
}

create_or_update_service "product-api" "http://product-api:8080"
create_or_update_route "product-api" "product-route" "/api/product"

create_or_update_service "order-api" "http://order-api:8080"
create_or_update_route "order-api" "order-route" "/api/order"

echo "Kong configuration complete."
