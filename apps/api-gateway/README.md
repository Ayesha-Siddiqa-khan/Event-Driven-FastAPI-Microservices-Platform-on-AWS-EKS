# api-gateway

FastAPI public entry point for the DevOps learning lab. The gateway accepts external user requests and forwards them to internal services. It does not connect directly to PostgreSQL, Redis, or SQS.

## Why This Service Is Public-Facing

Only the gateway should be exposed to users. It provides a stable public API while auth, order, and payment services remain internal implementation details.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness check for the gateway process. |
| `GET` | `/ready` | Readiness check for auth-service, order-service, and payment-service. |
| `GET` | `/metrics` | Prometheus metrics endpoint. |
| `POST` | `/api/register` | Forward to auth-service `/register`. |
| `POST` | `/api/login` | Forward to auth-service `/login`. |
| `POST` | `/api/orders` | Forward to order-service `/orders`. |
| `GET` | `/api/orders/{order_id}` | Forward to order-service `/orders/{order_id}`. |
| `POST` | `/api/payments/{order_id}` | Forward to payment-service `/payments/{order_id}`. |

## Environment Variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `SERVICE_NAME` | No | `api-gateway` | Service name used in health responses and logs. |
| `ENVIRONMENT` | No | `dev` | Runtime environment name used in health responses and logs. |
| `AUTH_SERVICE_URL` | Yes | `http://localhost:8001` | Base URL for auth-service. |
| `ORDER_SERVICE_URL` | Yes | `http://localhost:8002` | Base URL for order-service. |
| `PAYMENT_SERVICE_URL` | Yes | `http://localhost:8003` | Base URL for payment-service. |
| `REQUEST_TIMEOUT_SECONDS` | No | `5` | HTTP timeout for upstream service requests. |
| `LOG_LEVEL` | No | `INFO` | Root log level for structured JSON logs. |

## Internal Service Dependencies

- auth-service
- order-service
- payment-service

The gateway does not check or connect to PostgreSQL, Redis, or SQS directly.

## Request Forwarding Flow

1. A public request arrives at `/api/*`.
2. The gateway validates the public request shape.
3. The gateway forwards the request to the matching internal service endpoint.
4. Successful upstream responses are returned with the upstream status code and JSON body.
5. Upstream timeouts return `504`.
6. Upstream connection/request failures return `503`.

## Run Locally

From this directory:

```bash
cd apps/api-gateway
python -m pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Run Tests

The unit tests mock internal HTTP clients. They do not require real auth-service, order-service, or payment-service processes.

```bash
cd apps/api-gateway
python -m pytest -q
```

## Kubernetes Notes

This will be the only service exposed publicly through Kubernetes Ingress later. Internal services will be exposed only inside the Kubernetes cluster.

## TODO

- Add request correlation IDs and propagate them to internal services.
- Add authentication/authorization checks once token validation is part of the gateway contract.
