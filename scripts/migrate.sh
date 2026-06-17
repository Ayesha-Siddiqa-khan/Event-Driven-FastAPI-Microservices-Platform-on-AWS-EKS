#!/usr/bin/env bash
set -euo pipefail

SERVICES=(
  auth-service
  order-service
  payment-service
  notification-worker
)

for service in "${SERVICES[@]}"; do
  echo "Running Alembic migration for ${service}"
  (cd "apps/${service}" && alembic upgrade head)
done
