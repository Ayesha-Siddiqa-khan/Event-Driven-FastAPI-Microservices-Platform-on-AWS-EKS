# 09 - AWS Secrets Manager

Secrets Manager stores sensitive configuration.

## What should be secret?

Store these values in Secrets Manager:

```text
DATABASE_URL
REDIS_URL
JWT_SECRET
ORDER_EVENTS_QUEUE_URL if you prefer to treat it as config
NOTIFICATION_EVENTS_QUEUE_URL if you prefer to treat it as config
```

Queue URLs are not passwords, but storing them with other runtime config keeps configuration consistent.

## Secret naming pattern

```text
/edfp/dev/<service>/<secret-name>
```

Examples:

```text
/edfp/dev/auth-service/database-url
/edfp/dev/auth-service/redis-url
/edfp/dev/auth-service/jwt-secret
/edfp/dev/order-service/database-url
/edfp/dev/order-service/redis-url
/edfp/dev/order-service/order-events-queue-url
/edfp/dev/payment-service/database-url
/edfp/dev/payment-service/notification-events-queue-url
/edfp/dev/notification-worker/database-url
/edfp/dev/notification-worker/notification-events-queue-url
```

## How pods should receive secrets

You have two beginner-friendly options.

### Option A: External Secrets Operator

External Secrets Operator reads AWS Secrets Manager and creates Kubernetes Secrets.

Flow:

```text
AWS Secrets Manager
↓
External Secrets Operator
↓
Kubernetes Secret
↓
Pod environment variable
```

### Option B: Secrets Store CSI Driver with AWS provider

The CSI driver mounts secrets into pods as files.

Flow:

```text
AWS Secrets Manager
↓
CSI driver
↓
mounted files in pod
```

For this project, Option A is usually easier for environment variables.

## Do not store secrets in

```text
GitHub repository
Terraform variables committed to Git
Helm values files
Kubernetes ConfigMaps
Docker images
plain text documentation
```

## Secret-to-service mapping

| Service | Secrets needed |
|---|---|
| api-gateway | internal service URLs, optional shared token |
| auth-service | database-url, redis-url, jwt-secret |
| order-service | database-url, redis-url, order-events-queue-url |
| payment-service | database-url, notification-events-queue-url |
| notification-worker | database-url, notification-events-queue-url |

## Verification checklist

- secrets exist in Secrets Manager
- only required service account role can read each secret
- Kubernetes pods receive environment variables correctly
- no secret appears in GitHub
- no secret appears in container image
- application starts without hardcoded credentials
