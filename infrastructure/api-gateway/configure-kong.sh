#!/bin/bash

# Add product-api service
curl -i -X POST http://localhost:8001/services \
  --data name=product-api \
  --data url=http://product-api:8080

# Add product-api route
curl -i -X POST http://localhost:8001/services/product-api/routes \
  --data name=product-route \
  --data paths[]=/api/product \
  --data strip_path=false

# Add order-api service
curl -i -X POST http://localhost:8001/services \
  --data name=order-api \
  --data url=http://order-api:8080

# Add order-api route
curl -i -X POST http://localhost:8001/services/order-api/routes \
  --data name=order-route \
  --data paths[]=/api/order \
  --data strip_path=false
