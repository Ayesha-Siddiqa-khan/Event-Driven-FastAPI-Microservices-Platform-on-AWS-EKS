# 14 - Dev, Staging, and Production Values

Use different values per environment.

## Environment comparison

| Setting | Dev | Staging | Prod |
|---|---:|---:|---:|
| API replicas | 1 | 2 | 3+ |
| Worker min replicas | 1 | 1 | 2 |
| Worker max replicas | 3 | 5 | 10+ |
| RDS Multi-AZ | no | optional | yes |
| RDS backup retention | 1-3 days | 7 days | 14+ days |
| Redis replicas | 0 | 1 | 1+ |
| Manual approval | no | optional | yes |
| Debug logging | yes | no | no |
| Cost optimisation | high | medium | lower priority |

## Example app environment variables

Common:

```text
SERVICE_NAME=order-service
ENVIRONMENT=dev
AWS_REGION=us-east-1
```

Order service:

```text
DATABASE_URL=<from secrets>
REDIS_URL=<from secrets>
ORDER_EVENTS_QUEUE_URL=<from secrets or config>
```

Payment service:

```text
DATABASE_URL=<from secrets>
NOTIFICATION_EVENTS_QUEUE_URL=<from secrets or config>
```

Notification worker:

```text
DATABASE_URL=<from secrets>
NOTIFICATION_EVENTS_QUEUE_URL=<from secrets or config>
WORKER_POLL_INTERVAL_SECONDS=5
```

API gateway:

```text
AUTH_SERVICE_URL=http://auth-service.edfp-dev.svc.cluster.local:8000
ORDER_SERVICE_URL=http://order-service.edfp-dev.svc.cluster.local:8000
PAYMENT_SERVICE_URL=http://payment-service.edfp-dev.svc.cluster.local:8000
```

## Helm values files you should create later

```text
values-dev.yaml
values-staging.yaml
values-prod.yaml
```

## Promotion rule

Use the same image tag when promoting between environments:

```text
dev: a1b2c3d
staging: a1b2c3d
prod: a1b2c3d
```

Do not rebuild a different image for production after staging has passed. Build once, promote the same artefact.
