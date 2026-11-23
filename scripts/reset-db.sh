#!/usr/bin/env bash
set -e

echo "=== Resetting Database ==="
docker compose exec backend alembic downgrade base || true
docker compose exec backend alembic upgrade head
echo "Database migrations up to date."
