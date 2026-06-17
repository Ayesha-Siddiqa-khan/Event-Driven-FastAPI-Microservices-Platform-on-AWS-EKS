# 10 - IAM, OIDC, and IRSA

This project should use short-lived credentials and least-privilege IAM.

## GitHub Actions OIDC role

GitHub Actions should assume an AWS IAM role using OIDC.

Role name:

```text
edfp-dev-github-actions-deployer
```

This role should deploy infrastructure and push images.

Split roles later:

```text
edfp-dev-github-actions-infra
edfp-dev-github-actions-ecr-pusher
edfp-dev-github-actions-eks-deployer
```

## Kubernetes pod IAM access

For EKS workloads, use IRSA or EKS Pod Identity.

Do not put AWS access keys inside Kubernetes secrets.

## Recommended IAM roles for service accounts

| Kubernetes service account | IAM role | Purpose |
|---|---|---|
| `order-service-sa` | `edfp-dev-irsa-order-service` | send order SQS messages, read own secrets |
| `payment-service-sa` | `edfp-dev-irsa-payment-service` | send notification SQS messages, read own secrets |
| `notification-worker-sa` | `edfp-dev-irsa-notification-worker` | receive/delete notification messages, read own secrets |
| `auth-service-sa` | `edfp-dev-irsa-auth-service` | read database/redis/jwt secrets |

## Least privilege examples

Order service should access only:

```text
sqs:SendMessage on edfp-dev-order-events
sqs:GetQueueAttributes on edfp-dev-order-events
secretsmanager:GetSecretValue for /edfp/dev/order-service/*
```

Payment service should access only:

```text
sqs:SendMessage on edfp-dev-notification-events
sqs:GetQueueAttributes on edfp-dev-notification-events
secretsmanager:GetSecretValue for /edfp/dev/payment-service/*
```

Notification worker should access only:

```text
sqs:ReceiveMessage on edfp-dev-notification-events
sqs:DeleteMessage on edfp-dev-notification-events
sqs:ChangeMessageVisibility on edfp-dev-notification-events
sqs:GetQueueAttributes on edfp-dev-notification-events
secretsmanager:GetSecretValue for /edfp/dev/notification-worker/*
```

## Verification checklist

- GitHub Actions assumes AWS role through OIDC
- no AWS access keys are stored in GitHub secrets
- pods do not contain AWS access keys
- service accounts are mapped to IAM roles
- each service can access only the AWS resources it needs
- intentionally remove one permission and confirm the app fails as expected
