# EKS Deployment

EKS runs application workloads in private subnets. Only the API gateway is exposed publicly through Ingress.

Deployment order:

1. Create AWS infrastructure with Terraform.
2. Install External Secrets Operator.
3. Install KEDA.
4. Install AWS Load Balancer Controller if using ALB Ingress.
5. Build and push images to ECR.
6. Deploy Helm charts into `edfp-<env>`.
7. Run smoke tests.

Internal services stay behind ClusterIP services and are only reachable inside the cluster.

Helm deploys each service with:

- Deployment
- Service
- ServiceAccount
- ConfigMap for non-secret settings
- ExternalSecret for Secrets Manager values
- readiness/liveness probes
- resources
- migration Jobs for database services
