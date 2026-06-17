# Ingress

Only `api-gateway` should be exposed publicly.

The `helm/api-gateway` chart includes an ALB Ingress template. Install the AWS Load Balancer Controller before enabling it:

```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update
helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller \
  --namespace kube-system \
  --set clusterName=edfp-dev-eks \
  --set serviceAccount.create=true \
  --set serviceAccount.name=aws-load-balancer-controller
```

Internal services should remain `ClusterIP` and should not have public Ingress resources.
