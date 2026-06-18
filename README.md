# Event-Driven FastAPI Microservices Platform on AWS EKS

This repository is an **application-code-only starter project** for a DevOps deployment lab.

The goal is not to build a complex product. The goal is to practise deploying a realistic multi-service backend system using:

- FastAPI services
- PostgreSQL
- Redis
- AWS SQS
- background workers
- Kubernetes/EKS
- Helm
- GitHub Actions
- Prometheus/Grafana
- CloudWatch later
- queue-based worker autoscaling with KEDA


## App summary and expected output

A beginner-friendly explanation of what this app does and what output it should produce is available in [`APP_SUMMARY.md`](APP_SUMMARY.md).

For quick output examples, see [`docs/10-expected-app-output.md`](docs/10-expected-app-output.md).

## Important boundary

This ZIP intentionally does **not** include:

- Dockerfiles
- docker-compose
- Terraform
- Kubernetes YAML
- Helm charts
- GitHub Actions workflows
- AWS infrastructure code

You should create those yourself as part of your DevOps practice.

## Services

| Service | Type | PostgreSQL | Redis | SQS | Public |
|---|---|---:|---:|---:|---:|
| `api-gateway` | HTTP API | No | No | No | Yes |
| `auth-service` | HTTP API | Yes | Yes | No | Internal |
| `order-service` | HTTP API | Yes | Yes | Yes | Internal |
| `payment-service` | HTTP API | Yes | No | Yes | Internal |
| `notification-worker` | Background worker + health server | Yes | No | Yes | No |

## Repository structure

```text
apps/
  api-gateway/
  auth-service/
  order-service/
  payment-service/
  notification-worker/
docs/
  01-project-overview.md
  02-architecture.md
  03-service-contracts.md
  04-step-by-step-labs.md
  05-deployment-features.md
  06-monitoring-and-alerting.md
  07-failure-labs.md
  08-agent-prompt.md
  09-portfolio-checklist.md
  10-expected-app-output.md
```

## Recommended build order

1. Run `auth-service` locally with PostgreSQL and Redis.
2. Run `order-service` locally with PostgreSQL, Redis and SQS/LocalStack.
3. Run `payment-service` locally with PostgreSQL and SQS/LocalStack.
4. Run `notification-worker` locally and process SQS messages.
5. Add `api-gateway` after internal services work.
6. Then create your Dockerfiles.
7. Then create Terraform AWS infrastructure.
8. Then create Helm charts.
9. Then create GitHub Actions.
10. Then add KEDA, Prometheus, Grafana and failure labs.

## Local development note

For local SQS testing, use LocalStack or your real AWS SQS queues.
The application code supports:

```bash
SQS_ENDPOINT_URL=http://localhost:4566
```

For AWS SQS, leave `SQS_ENDPOINT_URL` empty.

## Ports suggestion

| Service | Suggested local port |
|---|---:|
| api-gateway | 8000 |
| auth-service | 8001 |
| order-service | 8002 |
| payment-service | 8003 |
| notification-worker health server | 8004 |

## What you should create yourself

You should create:

```text
Dockerfiles
Terraform modules
Helm charts
GitHub Actions workflows
KEDA ScaledObject
Prometheus ServiceMonitor
Grafana dashboard
CloudWatch alarms
```

This is where your DevOps learning will happen.


## Work division: agent vs you

This project now includes clear task separation:

- [`AGENT_TASKS.md`](AGENT_TASKS.md) — tasks for your FastAPI coding agent only.
- [`DEVOPS_TASKS_FOR_YOU.md`](DEVOPS_TASKS_FOR_YOU.md) — tasks you should do yourself as the DevOps engineer.
- [`docs/11-task-ownership-matrix.md`](docs/11-task-ownership-matrix.md) — side-by-side ownership table.
- [`docs/agent/01-service-by-service-prompts.md`](docs/agent/01-service-by-service-prompts.md) — prompts to give your coding agent one by one.
- [`docs/your-devops-work/01-agent-and-devops-workflow.md`](docs/your-devops-work/01-agent-and-devops-workflow.md) — workflow for combining agent code with your DevOps practice.
- [`docs/your-devops-work/02-your-devops-checklists.md`](docs/your-devops-work/02-your-devops-checklists.md) — checklists for Docker, AWS, EKS, Helm, CI/CD, monitoring and failure labs.

Simple rule:

```text
Agent = application code inside the container
You = Docker, AWS, Terraform, Kubernetes, Helm, CI/CD, scaling, monitoring and rollback
```

#test