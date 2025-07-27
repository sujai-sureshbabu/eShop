import json
import os
import time
import requests

KONG_ADMIN_URL = os.getenv("KONG_ADMIN_URL", "http://kong:8001")
CONFIG_FILE_PATH = os.getenv("KONG_CONFIG_FILE", "/kong-services.json")


def wait_for_kong():
    print("Waiting for Kong Admin API to be ready...")
    for _ in range(50):
        try:
            response = requests.get(f"{KONG_ADMIN_URL}/status")
            if response.status_code == 200:
                print("Kong Admin API is ready.")
                return
        except requests.RequestException:
            pass
        time.sleep(3)
    raise RuntimeError("Timed out waiting for Kong Admin API")


def create_or_update_service(service):
    print(f"Creating or updating service: {service['name']}")
    response = requests.put(f"{KONG_ADMIN_URL}/services/{service['name']}", json={
        "name": service["name"],
        "url": service["url"]
    })
    response.raise_for_status()


def create_or_update_route(service_name, route):
    print(f"Creating or updating route: {route['name']} for service: {service_name}")
    route_payload = {
        "name": route["name"],
        "paths": route["paths"],
        "service": {"name": service_name}
    }
    response = requests.put(f"{KONG_ADMIN_URL}/routes/{route['name']}", json=route_payload)
    response.raise_for_status()


def configure_plugins(route_name, plugins):
    for plugin in plugins:
        name = plugin["name"]
        config = plugin.get("config", {})
        print(f" Enabling plugin: {name} on route: {route_name}")

        existing = requests.get(f"{KONG_ADMIN_URL}/routes/{route_name}/plugins")
        if existing.status_code == 200 and any(p['name'] == name for p in existing.json().get('data', [])):
            print(f"Plugin {name} already exists on {route_name}, skipping.")
            continue

        plugin_payload = {"name": name, **({"config": config} if config else {})}
        response = requests.post(f"{KONG_ADMIN_URL}/routes/{route_name}/plugins", json=plugin_payload)
        response.raise_for_status()


def create_or_update_consumer():
    consumer = {
        "username": "demo-client",
        "custom_id": "client-001"
    }
    print("Creating or updating consumer: demo-client")
    requests.put(f"{KONG_ADMIN_URL}/consumers/demo-client", json=consumer)

    existing_creds = requests.get(f"{KONG_ADMIN_URL}/consumers/demo-client/jwt").json()
    if existing_creds.get("data"):
        
        print("JWT credentials already exist for demo-client")
        return

    print("Creating new JWT credentials for demo-client")
    jwt = {"algorithm": "HS256"}
    response = requests.post(f"{KONG_ADMIN_URL}/consumers/demo-client/jwt", data=jwt)
    response.raise_for_status()

    credentials = response.json()
    with open("demo-client-jwt.json", "w") as f:
        json.dump(credentials, f, indent=2)
    
    print("JWT credentials saved to demo-client-jwt.json")


def configure_kong():
    wait_for_kong()

    with open(CONFIG_FILE_PATH) as f:
        config = json.load(f)

    for service in config.get("services", []):
        create_or_update_service(service)
        for route in service.get("routes", []):
            create_or_update_route(service["name"], route)
            plugins = route.get("plugins", [])
            if plugins:
                configure_plugins(route["name"], plugins)

    create_or_update_consumer()


if __name__ == "__main__":
    configure_kong()