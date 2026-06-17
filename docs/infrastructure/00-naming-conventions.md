# 00 - Naming Conventions

Good naming is important because recruiters and engineers should understand your infrastructure quickly.

## Global naming variables

Use these base variables in Terraform later:

```text
project     = "edfp"
environment = "dev"
region      = "us-east-1"
owner       = "your-name"
managed_by  = "terraform"
```

## General resource naming pattern

```text
<project>-<environment>-<aws-service>-<purpose>
```

Examples:

```text
edfp-dev-vpc-main
edfp-dev-eks-main
edfp-dev-rds-postgres
edfp-dev-redis-main
edfp-dev-sqs-order-events
edfp-dev-sqs-notification-events
```

## S3 naming pattern

S3 bucket names must be globally unique. Include AWS account ID and region.

```text
<project>-<environment>-<purpose>-<account-id>-<region>
```

Examples:

```text
edfp-dev-tfstate-123456789012-us-east-1
edfp-dev-app-logs-123456789012-us-east-1
edfp-dev-db-backups-123456789012-us-east-1
```

Use lowercase letters, numbers, and hyphens only.

## ECR repository names

Create one ECR repository per service.

```text
edfp-dev-api-gateway
edfp-dev-auth-service
edfp-dev-order-service
edfp-dev-payment-service
edfp-dev-notification-worker
```

Image tags should be immutable and traceable:

```text
<git-sha>
<environment>-<git-sha>
<semantic-version>
```

Examples:

```text
dev-a1b2c3d
staging-a1b2c3d
v1.0.0
```

Avoid using only `latest` for real deployments.

## SQS queue names

Use standard queues first:

```text
edfp-dev-order-events
edfp-dev-notification-events
```

If you later use FIFO queues, the queue name must end with `.fifo`:

```text
edfp-dev-order-events.fifo
```

## Secrets Manager naming

Use path-style names:

```text
/edfp/dev/auth-service/database-url
/edfp/dev/auth-service/redis-url
/edfp/dev/order-service/database-url
/edfp/dev/order-service/redis-url
/edfp/dev/order-service/order-events-queue-url
/edfp/dev/payment-service/notification-events-queue-url
/edfp/dev/shared/jwt-secret
```

## IAM role names

Use clear service-account role names:

```text
edfp-dev-irsa-order-service
edfp-dev-irsa-payment-service
edfp-dev-irsa-notification-worker
edfp-dev-irsa-secrets-reader
edfp-dev-github-actions-deployer
```

## Kubernetes namespace names

Use one namespace per environment:

```text
edfp-dev
edfp-staging
edfp-prod
```

## Kubernetes service account names

```text
api-gateway-sa
auth-service-sa
order-service-sa
payment-service-sa
notification-worker-sa
```

## Tags for every AWS resource

Apply tags to all supported resources:

```text
Project     = edfp
Environment = dev
Owner       = your-name
ManagedBy   = terraform
CostCentre  = learning
Repository  = event-driven-fastapi-microservices-lab
```

These tags help with cost tracking, cleanup, and portfolio explanation.
