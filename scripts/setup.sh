#!/usr/bin/env bash
set -e

echo "=== Setting up FineExpert ==="
if [ ! -f backend/.env ]; then
  cp backend/.env.example backend/.env
  echo "Created backend/.env from template."
fi

if [ ! -f frontend/.env ]; then
  cp frontend/.env.example frontend/.env
  echo "Created frontend/.env from template."
fi

echo "Starting Docker Compose services..."
docker compose up -d --build
echo "FineExpert services are running!"
