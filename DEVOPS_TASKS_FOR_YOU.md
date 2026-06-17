# DEVOPS_TASKS_FOR_YOU.md

# Tasks for You as the DevOps Engineer

This file separates your work from the coding agent's work.

Your main job is to turn the application code into a real AWS/EKS deployment project.

You should create the infrastructure, CI/CD, containers, Helm charts, monitoring, autoscaling, rollback process, and portfolio evidence yourself.

---

# Your work boundary

You are responsible for creating and maintaining:

```text
Dockerfiles
Docker build strategy
Terraform modules
AWS infrastructure
ECR repositories
S3 remote state bucket
DynamoDB state lock table
EKS cluster
RDS PostgreSQL
ElastiCache Redis
SQS queues and DLQs
Secrets Manager secrets
IAM roles
OIDC integration
IRSA or EKS Pod Identity
Helm charts
Kubernetes manifests through Helm templates
KEDA autoscaling
Prometheus/Grafana monitoring
CloudWatch logs and alarms
GitHub Actions CI/CD
Load testing scripts
Failure labs
Portfolio screenshots and README evidence
```

---

# DevOps build order

Do not start with everything at once. Follow this order.

## Phase 1: Understand the app locally

Your tasks:

```text
1. Read APP_SUMMARY.md.
2. Read docs/10-expected-app-output.md.
3. Run each service locally.
4. Confirm /health works.
5. Confirm /ready behaviour.
6. Confirm PostgreSQL, Redis and SQS settings are environment-based.
```

Output evidence:

```text
Screenshots or terminal output for /health and /ready from each service.
```

---

## Phase 2: Containerise every service

Create Dockerfiles yourself for:

```text
api-gateway
auth-service
order-service
payment-service
notification-worker
```

Your goal:

```text
Each service has a small, repeatable image.
Each image uses environment variables.
Each image exposes the correct port.
Each image runs without editing source code.
```

Suggested image names:

```text
edfp-dev-api-gateway
edfp-dev-auth-service
edfp-dev-order-service
edfp-dev-payment-service
edfp-dev-notification-worker
```

Output evidence:

```text
docker build success screenshots
docker run health check screenshots
image size notes
```

---

## Phase 3: Create Terraform remote state

Create:

```text
S3 bucket for Terraform state
DynamoDB table for state locking
```

Suggested names:

```text
edfp-dev-tfstate-<aws-account-id>-<region>
edfp-dev-tflock
```

Your goal:

```text
Terraform state is not stored locally.
State locking protects you from parallel apply problems.
```

Output evidence:

```text
S3 bucket screenshot
DynamoDB table screenshot
terraform init success output
```

---

## Phase 4: Create AWS foundation infrastructure

Create Terraform modules for:

```text
VPC
public subnets
private subnets
NAT Gateway
route tables
security groups
IAM foundation roles
```

Suggested naming pattern:

```text
edfp-dev-vpc
edfp-dev-public-a
edfp-dev-private-a
edfp-dev-eks-sg
edfp-dev-rds-sg
edfp-dev-redis-sg
```

Output evidence:

```text
VPC diagram
subnet screenshot
security group screenshot
```

---

## Phase 5: Create ECR repositories

Create one ECR repository per service:

```text
edfp-dev-api-gateway
edfp-dev-auth-service
edfp-dev-order-service
edfp-dev-payment-service
edfp-dev-notification-worker
```

Image tag strategy:

```text
<git-sha>
<environment>-<git-sha>
```

Avoid:

```text
latest for production deployments
```

Output evidence:

```text
ECR repositories screenshot
first pushed image screenshot
```

---

## Phase 6: Create data services

Create:

```text
RDS PostgreSQL
ElastiCache Redis
SQS queues
SQS DLQs
Secrets Manager secrets
```

Suggested names:

```text
edfp-dev-rds-postgres
edfp-dev-redis-main
edfp-dev-order-events
edfp-dev-order-events-dlq
edfp-dev-notification-events
edfp-dev-notification-events-dlq
/edfp/dev/auth-service/database-url
/edfp/dev/auth-service/redis-url
/edfp/dev/order-service/database-url
/edfp/dev/order-service/redis-url
/edfp/dev/order-service/order-events-queue-url
/edfp/dev/payment-service/notification-events-queue-url
/edfp/dev/notification-worker/database-url
/edfp/dev/notification-worker/notification-events-queue-url
```

Output evidence:

```text
RDS screenshot
Redis screenshot
SQS queues screenshot
Secrets Manager screenshot with secret values hidden
```

---

## Phase 7: Create EKS cluster

Create:

```text
EKS cluster
managed node group or Karpenter later
OIDC provider
namespace per environment
```

Suggested names:

```text
edfp-dev-eks
namespace: edfp-dev
```

Install cluster components:

```text
AWS Load Balancer Controller
External Secrets Operator or your preferred secret sync method
metrics-server
KEDA
Prometheus stack
Grafana
```

Output evidence:

```text
kubectl get nodes
kubectl get ns
kubectl get pods -A
EKS console screenshot
```

---

## Phase 8: Create IAM for workloads

Create IAM permissions for services.

Minimum idea:

```text
order-service can send messages to order-events queue.
payment-service can send messages to notification-events queue.
notification-worker can receive and delete messages from notification-events queue.
services can read only their own required secrets.
```

Suggested names:

```text
edfp-dev-irsa-order-service
edfp-dev-irsa-payment-service
edfp-dev-irsa-notification-worker
edfp-dev-irsa-external-secrets
```

Output evidence:

```text
IAM role screenshot
trust policy screenshot
service account annotation screenshot
```

---

## Phase 9: Create Helm charts

Create Helm charts yourself.

Recommended structure:

```text
helm/
  api-gateway/
  auth-service/
  order-service/
  payment-service/
  notification-worker/
```

Every API service chart should support:

```text
Deployment
Service
ConfigMap
Secret reference
readinessProbe
livenessProbe
resources
HPA
ServiceMonitor if using Prometheus Operator
```

Worker chart should support:

```text
Deployment
no public Ingress
readinessProbe
livenessProbe
resources
KEDA ScaledObject
ServiceMonitor if exposing metrics
```

Output evidence:

```text
helm lint output
helm template output
helm upgrade --install output
kubectl get deploy,svc,pods
```

---

## Phase 10: Deploy services in the correct order

Deploy in this order:

```text
1. auth-service
2. order-service
3. payment-service
4. notification-worker
5. api-gateway
```

Before each deployment:

```text
Run database migration if the service uses PostgreSQL.
```

After each deployment:

```text
Check /health.
Check /ready.
Check pod logs.
Check metrics endpoint.
```

Output evidence:

```text
kubectl rollout status deployment/<service>
curl /health result
curl /ready result
```

---

## Phase 11: Build GitHub Actions CI/CD

Create workflows for:

```text
pull request validation
build and push Docker images to ECR
deploy to dev
deploy to staging
deploy to production with approval
migration before deployment
smoke test after deployment
rollback after failed smoke test
```

Use:

```text
GitHub Actions OIDC to AWS
no long-lived AWS keys
image tag = Git SHA
```

Output evidence:

```text
GitHub Actions pipeline screenshot
OIDC role screenshot
successful deployment screenshot
failed deployment rollback screenshot
```

---

## Phase 12: Add KEDA queue autoscaling

Scale `notification-worker` based on SQS queue depth.

Beginner settings:

```text
min replicas: 1
max replicas: 5
queue length threshold: 5
```

Test:

```text
Send many messages to notification-events queue.
Watch worker replicas increase.
Watch queue depth decrease.
Watch worker replicas decrease.
```

Output evidence:

```text
SQS queue depth screenshot
kubectl get hpa or scaledobject screenshot
worker replica count before/after screenshot
```

---

## Phase 13: Add monitoring

Start with:

```text
Prometheus
Grafana
```

Then add:

```text
CloudWatch logs
CloudWatch alarms
```

Dashboards should show:

```text
API latency
HTTP error rate
request count
pod restarts
CPU and memory
worker processed messages
worker failed messages
SQS queue depth
PostgreSQL connections
Redis availability
```

Output evidence:

```text
Grafana dashboard screenshot
Prometheus targets screenshot
CloudWatch logs screenshot
CloudWatch alarm screenshot
```

---

## Phase 14: Add load testing

Use k6 first.

Test:

```text
register users
create orders
create payments
send many notifications
```

Record:

```text
requests per second
p95 latency
error rate
queue depth
worker replica count
```

Output evidence:

```text
k6 result screenshot
Grafana during load test screenshot
KEDA scaling screenshot
```

---

## Phase 15: Add rollback and failure labs

Run these labs:

```text
Bad image rollback
Bad readiness check
Wrong DB password
Redis unavailable
High queue depth
Pod crash
High API traffic
```

For each lab, document:

```text
what was broken
how the system reacted
how you detected it
how you fixed it
screenshot evidence
lesson learnt
```

Output evidence:

```text
failure-lab screenshots
rollback command/output
GitHub Actions failed and recovered pipeline screenshot
```

---

# Your final portfolio checklist

At the end, your repository should show:

```text
[ ] App code from agent
[ ] Dockerfiles created by you
[ ] Terraform modules created by you
[ ] ECR repositories
[ ] EKS deployment
[ ] RDS PostgreSQL
[ ] ElastiCache Redis
[ ] SQS queues and DLQs
[ ] Secrets Manager
[ ] IAM OIDC/IRSA
[ ] Helm charts
[ ] GitHub Actions CI/CD
[ ] Database migration before deployment
[ ] KEDA queue autoscaling
[ ] Prometheus/Grafana dashboard
[ ] CloudWatch logs/alarms
[ ] Load testing results
[ ] Rollback demo
[ ] Failure lab documentation
[ ] Architecture diagram
[ ] Cost and cleanup notes
```
