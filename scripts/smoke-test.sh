#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${ENVIRONMENT:-dev}"
NAMESPACE="${NAMESPACE:-edfp-${ENVIRONMENT}}"
GATEWAY_URL="${GATEWAY_URL:-}"

if [[ -n "${GATEWAY_URL}" ]]; then
  curl -fsS "${GATEWAY_URL}/health"
  curl -fsS "${GATEWAY_URL}/ready"
else
  kubectl -n "${NAMESPACE}" run smoke-api-gateway \
    --rm -i --restart=Never --image=curlimages/curl:8.10.1 -- \
    sh -c "curl -fsS http://edfp-${ENVIRONMENT}-api-gateway:8000/health && curl -fsS http://edfp-${ENVIRONMENT}-api-gateway:8000/ready"
fi

for service in auth-service order-service payment-service; do
  kubectl -n "${NAMESPACE}" run "smoke-${service}" \
    --rm -i --restart=Never --image=curlimages/curl:8.10.1 -- \
    curl -fsS "http://edfp-${ENVIRONMENT}-${service}:8000/health"
done

echo "Smoke tests passed for ${NAMESPACE}"
