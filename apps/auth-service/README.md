# auth-service

FastAPI authentication service for the DevOps learning lab. It stores users in PostgreSQL and writes fake login sessions to Redis using keys in the form `session:{token}`.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness check for the service process. |
| `GET` | `/ready` | Readiness check for PostgreSQL and Redis. |
| `GET` | `/metrics` | Prometheus metrics exposition endpoint. |
| `POST` | `/register` | Create a user with a hashed password. |
| `POST` | `/login` | Validate credentials and create a Redis-backed fake session. |
| `GET` | `/users/{user_id}` | Return public user information. |

## Environment Variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `SERVICE_NAME` | No | `auth-service` | Name returned by `/health` and included in logs. |
| `ENVIRONMENT` | No | `dev` | Runtime environment name included in health and logs. |
| `DATABASE_URL` | Yes | `postgresql://postgres:postgres@localhost:5432/devops_lab` | SQLAlchemy PostgreSQL connection URL. |
| `REDIS_URL` | Yes | `redis://localhost:6379/0` | Redis connection URL. |
| `SESSION_TTL_SECONDS` | No | `3600` | Redis TTL for fake session tokens. |
| `LOG_LEVEL` | No | `INFO` | Root log level for JSON logs. |

## Database

The service expects a `users` table with:

- `id`
- `email`
- `password_hash`
- `created_at`

Alembic migrations live in `migrations/`.

## Run Locally

From this directory:

```bash
cd apps/auth-service
python -m pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## Run Tests

The unit tests use SQLite and a fake Redis dependency override, so they do not need live PostgreSQL or Redis.

```bash
cd apps/auth-service
python -m pytest -q
```

## Logging and Metrics

Logs are emitted as structured JSON with service and environment metadata. Prometheus metrics include HTTP request counts, latency histograms, registration count, login success count, login failure count, and user lookup count.

## TODO

- Add token-authenticated endpoints when the lab needs protected routes.
- Add rate limiting for login attempts if this becomes more than a fake learning service.
