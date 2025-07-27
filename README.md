# eShop Microservices Starter Kit

A production-ready microservices starter kit built with .NET 9, Kafka, PostgreSQL, Kong API Gateway, and OpenTelemetry for full observability.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Architecture](#project-architecture)
- [Infrastructure Components](#infrastructure-components)
- [Running the Project](#running-the-project)
- [Testing the APIs](#testing-the-apis)
- [Observability](#observability)
- [Configuration & Environment Variables](#configuration--environment-variables)
- [Extending the Project](#extending-the-project)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Tech Stack

- **Backend:** .NET 9 (C#) microservices
- **API Gateway:** Kong (open-source)
- **Messaging:** Apache Kafka (event-driven architecture)
- **Databases:** PostgreSQL (relational)
- **Observability:** OpenTelemetry Collector, Jaeger (distributed tracing), Prometheus (metrics), Grafana (dashboards)
- **Containerization:** Docker & Docker Compose

---

## Prerequisites

- Docker (v20+)
- Docker Compose (v2+)
- Git
- Basic familiarity with Docker and HTTP APIs

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/your-username/eshop-microservices.git
cd eshop-microservices
```

---

## Project Architecture

| Component        | Responsibility                      |
|------------------|-------------------------------------|
| Product API      | Product catalog REST API            |
| Order API        | Order REST API                      |
| Order Service    | Business logic & saga orchestration |
| Kafka            | Event messaging                     |
| PostgreSQL       | Data persistence                    |
| Kong API Gateway | Routing and API management          |
| OpenTelemetry    | Telemetry aggregation               |
| Jaeger           | Distributed tracing UI              |
| Prometheus       | Metrics collection                  |
| Grafana          | Visualization dashboards            |

---

## Infrastructure Components

| Component                  | Description                                   |
|----------------------------|-----------------------------------------------|
| **Kafka (broker)**         | Event streaming platform for messaging        |
| **PostgreSQL**             | Two databases: Kong DB and Order DB           |
| **Kong**                   | API Gateway for routing and API management    |
| **OpenTelemetry Collector**| Aggregates and exports telemetry data         |
| **Jaeger**                 | Distributed tracing user interface            |
| **Prometheus**             | Metrics collection and monitoring             |
| **Grafana**                | Visualization dashboards for observability    |

---

## Running the Project

**Step 1:** Start all containers

```bash
docker compose up -d
```

---

## Testing the APIs

### Direct Access

- **Product API:**
    ```bash
    curl http://localhost:5001/api/product
    ```
- **Order API:**
    ```bash
    curl http://localhost:5005/api/order
    ```

### Through Kong API Gateway

- **Product API:**
    ```bash
    curl http://localhost:8000/api/product
    ```
- **Order API:**
    ```bash
    curl http://localhost:8000/api/order
    ```

### 🔐 JWT Authentication Setup

This project configures Kong API Gateway with JWT-based authentication for securing service routes.

#### ✅ What This Adds

- JWT plugin is enabled on `product-api` and `order-api` routes
- A consumer named `demo-client` is created automatically
- JWT credentials (key/secret) are generated for this consumer
- Tokens can be signed and used to access protected APIs

#### 🛠 How It Works

1. Kong's `jwt` plugin checks for a valid Bearer token
2. The token must be signed using the consumer's secret
3. Only valid tokens will be allowed through the protected route

---

## Observability

- **Jaeger UI:** [http://localhost:16686](http://localhost:16686) — Distributed tracing visualization
<img width="1913" height="949" alt="image" src="https://github.com/user-attachments/assets/8dd32da3-356b-4b23-8de3-426900594268" />


- **Prometheus UI:** [http://localhost:9090](http://localhost:9090) — Metrics collection and querying
<img width="1913" height="529" alt="image" src="https://github.com/user-attachments/assets/2d290907-4267-40d5-b2f1-943ebc8040d3" />

- **Grafana UI:** [http://localhost:3000](http://localhost:3000) — Dashboards for metrics and traces
<img width="1913" height="949" alt="image" src="https://github.com/user-attachments/assets/865db886-1aaa-4e48-a3d1-2212f11a4e3d" />

---

## Extending the Project

To add a new service:

1. **Create the Service:**  
   Scaffold your new service/api following the existing project structure.
2. **Update Docker Compose:**  
   Add the new service to `docker-compose.yml` with its build context and required environment variables.
3. **Configure Kong:**  
   Edit `kong-init.sh` to register the new service and its route(s) using create_or_update_service , create_or_update_route.
4. **Apply Kong Configuration:**  
   The `kong-init` container will automatically run the updated script when you restart the stack.
5. **Rebuild and Start:**  
   Rebuild and start the containers:
   ```bash
   docker compose up -d --build
   ```

Your new service should now be accessible through the API Gateway.

---

## Troubleshooting

**Kong 404 or missing routes:**  
Check registered routes and services:
```bash
curl http://localhost:8001/routes
curl http://localhost:8001/services
```

**Conflict errors on Kong config:**  
Delete existing services/routes or patch them as needed.

**Kafka topic issues:**  
Check `kafka-init` logs or manually create topics inside the Kafka container.

**Port conflicts:**  
Ensure required ports are free or update them in `docker-compose.yml`.

**View logs:**
```bash
docker logs <container-name>
```

---

## Contributing

Contributions and improvements are welcome! Please open issues or pull requests.

---

## License

MIT License

---

Developed by Sujai Sureshbabu — A full microservices starter kit with observability, API Gateway, and event-driven design.
