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

aws ecr get-login-password --region "${AWS_REGION}" \
  | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

for service in "${SERVICES[@]}"; do
  repo="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/edfp-${ENVIRONMENT}-${service}"
  echo "Pushing ${repo}:${GIT_SHA} and ${repo}:${ENVIRONMENT}"
  docker push "${repo}:${GIT_SHA}"
  docker push "${repo}:${ENVIRONMENT}"
  if [[ "${ENVIRONMENT}" == "dev" ]]; then
    docker push "${repo}:latest"
  fi
done
