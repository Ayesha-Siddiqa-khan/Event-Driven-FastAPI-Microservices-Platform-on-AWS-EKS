# Cost and Cleanup

This project creates paid AWS resources. Watch these first:

- NAT Gateway hourly and data processing charges
- EKS cluster hourly charges
- RDS instance and storage
- ElastiCache nodes
- Load balancers

Cleanup dev:

```bash
helm uninstall edfp-dev-api-gateway -n edfp-dev || true
helm uninstall edfp-dev-notification-worker -n edfp-dev || true
helm uninstall edfp-dev-payment-service -n edfp-dev || true
helm uninstall edfp-dev-order-service -n edfp-dev || true
helm uninstall edfp-dev-auth-service -n edfp-dev || true

cd infra/terraform/envs/dev
terraform destroy
```

After destroy, check:

- ECR old images
- Load balancers
- NAT gateways
- RDS snapshots
- CloudWatch log groups
