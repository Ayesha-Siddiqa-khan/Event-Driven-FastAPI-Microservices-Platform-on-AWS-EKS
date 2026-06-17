# KEDA

Install KEDA before deploying `notification-worker`:

```bash
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm upgrade --install keda kedacore/keda \
  --namespace keda \
  --create-namespace \
  --set serviceAccount.operator.annotations."eks\\.amazonaws\\.com/role-arn"=REPLACE_WITH_KEDA_IRSA_ROLE_ARN
```

The `notification-worker` chart includes a `ScaledObject` that scales on the notification SQS queue depth. Dev defaults to 1-3 replicas, staging to 1-5, and prod to 1-10.
