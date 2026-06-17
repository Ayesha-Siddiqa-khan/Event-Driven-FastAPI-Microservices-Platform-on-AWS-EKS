# 06 - RDS PostgreSQL

RDS PostgreSQL stores the project data.

## Recommended beginner design

Use one RDS PostgreSQL instance for the first version.

Name:

```text
edfp-dev-rds-postgres
```

Database name:

```text
edfp_dev
```

Username:

```text
edfp_app
```

Do not hardcode the password. Store it in AWS Secrets Manager.

## Tables created by services

| Service | Table |
|---|---|
| auth-service | `users` |
| order-service | `orders` |
| payment-service | `payments` |
| notification-worker | `notifications` |

## Recommended RDS settings for dev

```text
engine: PostgreSQL
public access: no
subnets: private-db-a, private-db-b
security group: edfp-dev-sg-rds-postgres
backup retention: 1-7 days
multi-az: optional for dev, recommended for prod
storage encryption: enabled
```

## Production improvement

For production-like deployment:

```text
multi-az: enabled
backup retention: 7-14 days
deletion protection: enabled
performance insights: enabled
```

## Security group rule

Allow inbound only from EKS app security group:

```text
source: edfp-dev-sg-eks-apps
port: 5432
protocol: TCP
```

Never expose RDS publicly for this project.

## Secret value format

Store database URL as:

```text
postgresql+psycopg2://edfp_app:<password>@<rds-endpoint>:5432/edfp_dev
```

Secrets Manager names:

```text
/edfp/dev/auth-service/database-url
/edfp/dev/order-service/database-url
/edfp/dev/payment-service/database-url
/edfp/dev/notification-worker/database-url
```

For beginner version, these can all contain the same database URL.

## Migration strategy

Each service has its own Alembic migration folder.

Deployment order:

```text
run migration
then deploy app
then smoke test
```

Do not deploy new code before the required migration succeeds.

## Verification checklist

- RDS instance is available
- RDS is not publicly accessible
- EKS pods can connect to port 5432
- local machine cannot connect unless using a bastion/port-forward/VPN
- `alembic upgrade head` works from a migration job
- `/ready` endpoint reports PostgreSQL as healthy
- automated backups are enabled
