# 04 - Step-by-Step Labs

## Lab 1 - auth-service locally

Goal: learn PostgreSQL + Redis + FastAPI readiness checks.

Tasks:

1. Create PostgreSQL database.
2. Create Redis instance.
3. Set `DATABASE_URL` and `REDIS_URL`.
4. Install requirements.
5. Run Alembic migration.
6. Start service.
7. Test `/health`.
8. Test `/ready`.
9. Register a user.
10. Login and verify Redis session.

## Lab 2 - order-service locally

Goal: learn PostgreSQL + Redis + SQS publishing.

Tasks:

1. Create `order-events-queue` in AWS SQS or LocalStack.
2. Set `ORDER_EVENTS_QUEUE_URL`.
3. Run migration.
4. Start service.
5. Create order.
6. Check PostgreSQL order row.
7. Check Redis cached order.
8. Check SQS message.

## Lab 3 - payment-service locally

Goal: learn SQS publishing from another service.

Tasks:

1. Create `notification-events-queue`.
2. Set `NOTIFICATION_EVENTS_QUEUE_URL`.
3. Run migration.
4. Start service.
5. Create payment.
6. Check payment row.
7. Check SQS notification message.

## Lab 4 - notification-worker locally

Goal: learn background worker processing.

Tasks:

1. Start notification-worker.
2. Send message to `notification-events-queue`.
3. Verify worker consumes message.
4. Verify notification row is saved.
5. Verify message is deleted after success.
6. Check `/metrics`.

## Lab 5 - api-gateway locally

Goal: learn internal service calls.

Tasks:

1. Start auth-service, order-service and payment-service.
2. Start api-gateway.
3. Register user through gateway.
4. Create order through gateway.
5. Create payment through gateway.

## Lab 6 - containerisation

Create Dockerfiles yourself. Each service should:

- install requirements
- expose its port
- start with uvicorn
- use environment variables

## Lab 7 - Terraform

Create AWS resources yourself:

- VPC
- EKS
- ECR
- RDS PostgreSQL
- ElastiCache Redis
- SQS queues
- IAM roles
- Secrets Manager

## Lab 8 - Helm

Create Helm charts yourself:

- one chart per service or one umbrella chart
- separate values for dev, staging and production
- probes
- resources
- autoscaling
- secrets references

## Lab 9 - GitHub Actions

Create workflows yourself:

- PR checks
- build and push images
- migrations
- deploy to dev
- deploy to staging
- manual approval for production
- smoke test
- rollback on failure

## Lab 10 - KEDA autoscaling

Add KEDA for `notification-worker`.

Test:

1. Send many messages to SQS.
2. Watch worker replicas increase.
3. Watch queue depth decrease.
4. Watch worker replicas scale down.
