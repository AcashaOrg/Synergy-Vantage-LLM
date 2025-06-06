#!/usr/bin/env bash
# smoke_test.sh - build and test the local API container
set -euo pipefail

IMAGE="synergy-api-local"
CONTAINER="synergy-api-smoke"

# Build the Docker image

docker build -t "$IMAGE" -f api/Dockerfile .

# Run the container in detached mode
CID=$(docker run -d --rm --name "$CONTAINER" -p 8000:8000 "$IMAGE")

# Wait for server to start
sleep 5

# Query the /generate endpoint
curl -s -H "x-api-key: demo-key-123" \
     -H "Content-Type: application/json" \
     -d '{"prompt":"ping"}' \
     http://localhost:8000/generate

docker stop "$CID" >/dev/null
