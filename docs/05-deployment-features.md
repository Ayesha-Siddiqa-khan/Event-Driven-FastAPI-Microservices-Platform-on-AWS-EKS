# 05 - Deployment Features

## Separate API and worker deployments

API services:

```text
api-gateway
auth-service
order-service
payment-service
```

Worker service:

```text
notification-worker
```

The worker should not have public Ingress.

## Database migration before deployment

Recommended deployment order:

```text
1. Build image
2. Push image
3. Run Alembic migration job
4. Deploy with Helm
5. Run smoke test
6. Rollback if smoke test fails
```

Do not deploy app code that expects a new database table before the migration succeeds.

## Environments

Create these Helm values files yourself:

```text
values-dev.yaml
values-staging.yaml
values-prod.yaml
```

Suggested differences:

| Environment | Replicas | Logging | Approval |
|---|---:|---|---|
| dev | 1 | debug | no |
| staging | 2 | info | no/manual optional |
| production | 3+ | warning/info | yes |

## Rollback strategy

For each service:

1. Deploy new image.
2. Run readiness check.
3. Run smoke test.
4. If failed, run Helm rollback.
5. Keep screenshots of failed deployment and successful rollback.

## Secrets strategy

Use AWS Secrets Manager for:

```text
DATABASE_URL
REDIS_URL
JWT_SECRET
```

Do not store secrets in:

- GitHub repository
- Helm values files
- Docker images
- Kubernetes ConfigMaps
