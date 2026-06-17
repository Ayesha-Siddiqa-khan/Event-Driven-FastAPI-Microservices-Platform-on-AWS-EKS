#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${ENVIRONMENT:-dev}"
AWS_REGION="${AWS_REGION:-us-east-1}"
GIT_SHA="${GIT_SHA:-$(git rev-parse --short HEAD)}"
AWS_ACCOUNT_ID="${AWS_ACCOUNT_ID:-$(aws sts get-caller-identity --query Account --output text)}"

SERVICES=(
  api-gateway
  auth-service
  order-service
  payment-service
  notification-worker
)

for service in "${SERVICES[@]}"; do
  repo="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/edfp-${ENVIRONMENT}-${service}"
  echo "Building ${repo}:${GIT_SHA}"
  docker build -t "${repo}:${GIT_SHA}" -t "${repo}:${ENVIRONMENT}" "apps/${service}"
  if [[ "${ENVIRONMENT}" == "dev" ]]; then
    docker tag "${repo}:${GIT_SHA}" "${repo}:latest"
  fi
done
