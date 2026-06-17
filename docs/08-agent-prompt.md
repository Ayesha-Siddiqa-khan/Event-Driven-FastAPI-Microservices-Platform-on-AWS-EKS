# 08 - Agent Prompt

Use this prompt if you want a coding agent to regenerate or improve only the application code.

```text
You are a senior Python backend engineer. Generate application code only for an event-driven FastAPI microservices project. Do not create Dockerfiles, Kubernetes manifests, Helm charts, Terraform files, GitHub Actions workflows, cloud infrastructure files, or deployment files.

Project goal:
Create functional FastAPI services for a DevOps deployment lab. The application logic should be simple, but the services must be realistic enough to deploy on Kubernetes with PostgreSQL, Redis, AWS SQS, Prometheus metrics, health checks, readiness checks, and background workers.

Create this app-only structure:

apps/
  api-gateway/
  auth-service/
  order-service/
  payment-service/
  notification-worker/

Each service must be independent and have its own requirements.txt and README.md.

Global requirements:
1. Use FastAPI.
2. Use Pydantic settings for environment variables.
3. Add /health, /ready, and /metrics endpoints to every HTTP service.
4. Use prometheus-fastapi-instrumentator or prometheus-client for metrics.
5. Use structured JSON logging.
6. Use PostgreSQL with SQLAlchemy or SQLModel where database is needed.
7. Use Alembic migrations where database is needed.
8. Use Redis where cache/session is needed.
9. Use boto3 for AWS SQS client code.
10. SQS client must support optional SQS_ENDPOINT_URL for local testing with LocalStack.
11. Code must read all secrets and configuration from environment variables.
12. Do not hardcode credentials.
13. Add basic error handling.
14. Add simple pytest tests for health/readiness where reasonable.
15. Keep business logic simple. The focus is deployable service behaviour.
```

## Service-by-service prompts

For safer step-by-step work, use [`docs/agent/01-service-by-service-prompts.md`](agent/01-service-by-service-prompts.md). These prompts separate each service so your coding agent only works on application code and does not create Docker, Terraform, Kubernetes, Helm, or GitHub Actions files.

