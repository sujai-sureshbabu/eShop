# This Dockerfile sets up a Python environment to run the Kong initialization script.
# It copies the necessary files into the container, installs the required dependencies,
# and specifies the command to run the script when the container starts.

FROM python:3.11-alpine

WORKDIR /app

COPY kong_init.py .
COPY kong-services.json /kong-services.json

RUN pip install requests
CMD ["python", "kong_init.py"]
