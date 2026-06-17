# Secrets Management

Application secrets live in AWS Secrets Manager under:

```text
/edfp/<env>/<service>/<secret-name>
```

Examples:

- `/edfp/dev/auth-service/database-url`
- `/edfp/dev/order-service/order-events-queue-url`
- `/edfp/dev/api-gateway/auth-service-url`

External Secrets Operator syncs AWS Secrets Manager values into Kubernetes Secrets. Kubernetes ConfigMaps are used only for non-secret configuration such as `SERVICE_NAME`, `ENVIRONMENT`, and log levels.

Do not commit `.env` files or secret values.
