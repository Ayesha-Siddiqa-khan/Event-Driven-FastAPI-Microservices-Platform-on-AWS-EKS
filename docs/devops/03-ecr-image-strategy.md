# ECR Image Strategy

Terraform creates one ECR repository per service per environment:

- `edfp-dev-api-gateway`
- `edfp-dev-auth-service`
- `edfp-dev-order-service`
- `edfp-dev-payment-service`
- `edfp-dev-notification-worker`

The same pattern applies to staging and prod.

Images are tagged with:

- Git SHA, for immutable deployment references
- environment tag, such as `dev`
- `latest` only for dev convenience

Example:

```text
<account-id>.dkr.ecr.us-east-1.amazonaws.com/edfp-dev-order-service:<git-sha>
```
