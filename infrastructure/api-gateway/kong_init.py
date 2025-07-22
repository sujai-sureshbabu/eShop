import requests
import json
import time

KONG_ADMIN_URL = "http://kong:8001"
KONG_CONFIG_FILE = "/kong-services.json"


def wait_for_kong():
    print("Waiting for Kong Admin API...")
    while True:
        try:
            response = requests.get(f"{KONG_ADMIN_URL}/status")
            if response.status_code == 200 and response.json().get("database", {}).get("reachable"):
                print("Kong Admin API is ready.")
                return
        except requests.exceptions.RequestException:
            pass
        print("Kong not ready. Retrying in 3s...")
        time.sleep(3)


def create_or_update_service(service):
    name = service["name"]
    url = service["url"]

    resp = requests.get(f"{KONG_ADMIN_URL}/services/{name}")
    if resp.status_code == 404:
        print(f"* Creating service: {name}")
        requests.post(f"{KONG_ADMIN_URL}/services", data={"name": name, "url": url})
    else:
        print(f"* Updating service: {name}")
        requests.patch(f"{KONG_ADMIN_URL}/services/{name}", data={"url": url})


def create_or_update_route(service_name, route):
    route_name = route["name"]
    paths = route["paths"]
    data = {"name": route_name}
    for p in paths:
        data.setdefault("paths[]", []).append(p)

    resp = requests.get(f"{KONG_ADMIN_URL}/services/{service_name}/routes/{route_name}")
    if resp.status_code == 404:
        print(f"* Creating route: {route_name}")
        requests.post(f"{KONG_ADMIN_URL}/services/{service_name}/routes", data=data)
    else:
        print(f"* Updating route: {route_name}")
        requests.patch(f"{KONG_ADMIN_URL}/services/{service_name}/routes/{route_name}", data=data)


def attach_plugins(route_name, plugins):
    for plugin in plugins:
        name = plugin["name"]
        config = plugin.get("config", {})
        print(f"Attaching plugin: {name} to route: {route_name}")
        resp = requests.post(
            f"{KONG_ADMIN_URL}/routes/{route_name}/plugins",
            json={"name": name, "config": config}
        )
        if resp.status_code in [200, 201, 409]:
            print(f"Plugin {name} attached.")
        else:
            print(f"Failed to attach plugin {name}: {resp.text}")


def configure_kong():
    with open(KONG_CONFIG_FILE) as f:
        config = json.load(f)

    for service in config.get("services", []):
        create_or_update_service(service)
        for route in service.get("routes", []):
            create_or_update_route(service["name"], route)
            if "plugins" in route:
                attach_plugins(route["name"], route["plugins"])


if __name__ == "__main__":
    wait_for_kong()
    configure_kong()
    print("Kong configuration complete.")
