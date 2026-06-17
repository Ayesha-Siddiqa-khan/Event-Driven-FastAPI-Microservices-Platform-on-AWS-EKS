# Helm

Each service has its own Helm chart:

- `api-gateway`
- `auth-service`
- `order-service`
- `payment-service`
- `notification-worker`

The API gateway chart includes public Ingress. All other services use `ClusterIP`.

Database services include Helm hook migration Jobs that run `alembic upgrade head` before install/upgrade. Do not run migrations in normal application startup.
