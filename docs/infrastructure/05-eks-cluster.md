# 05 - EKS Cluster

Amazon EKS runs your FastAPI services and background worker on Kubernetes.

## Cluster name

```text
edfp-dev-eks-main
```

## Kubernetes namespaces

Create one namespace for the dev environment:

```text
edfp-dev
```

Later:

```text
edfp-staging
edfp-prod
```

## Node group

Start with one managed node group.

Name:

```text
edfp-dev-ng-apps
```

Recommended beginner size:

```text
instance type: t3.medium or t3.large
min nodes: 1
max nodes: 3
desired nodes: 2
```

If cost is a concern, use smaller capacity, but monitoring and multiple services may need more memory.

## Add-ons and controllers

Install these after the cluster is ready:

| Component | Purpose |
|---|---|
| VPC CNI | pod networking |
| CoreDNS | cluster DNS |
| kube-proxy | Kubernetes networking |
| EBS CSI driver | persistent volumes if needed |
| AWS Load Balancer Controller | create ALB from Ingress |
| Metrics Server | HPA metrics |
| KEDA | queue-based worker autoscaling |
| Prometheus | app metrics scraping |
| Grafana | dashboards |
| External Secrets or Secrets Store CSI | connect Secrets Manager to Kubernetes |

## Workload deployment model

Deploy API services as Kubernetes Deployments:

```text
api-gateway
auth-service
order-service
payment-service
```

Deploy worker service separately:

```text
notification-worker
```

Only `api-gateway` should have public ingress.

Internal services should be reachable by Kubernetes service DNS names:

```text
auth-service.edfp-dev.svc.cluster.local
order-service.edfp-dev.svc.cluster.local
payment-service.edfp-dev.svc.cluster.local
```

## Recommended Kubernetes service accounts

```text
api-gateway-sa
auth-service-sa
order-service-sa
payment-service-sa
notification-worker-sa
```

Map service accounts to IAM roles only where AWS permissions are needed.

## Which services need AWS permissions?

| Service | Needs AWS access? | Permissions |
|---|---:|---|
| api-gateway | no, unless reading secrets directly | usually none |
| auth-service | maybe | Secrets Manager only |
| order-service | yes | SQS send, Secrets Manager |
| payment-service | yes | SQS send, Secrets Manager |
| notification-worker | yes | SQS receive/delete, Secrets Manager |

## Verification checklist

- EKS cluster is active
- nodes are ready
- namespace exists
- CoreDNS is healthy
- metrics-server works
- AWS Load Balancer Controller is installed
- pods can resolve internal service DNS
- pods can reach RDS and Redis
- service accounts are annotated or associated correctly for AWS access
