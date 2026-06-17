# 01 - Project Overview

## Goal

Build and deploy an event-driven FastAPI microservices system where:

- Some services are HTTP APIs.
- Some services use PostgreSQL.
- Some services use Redis.
- Some services publish SQS messages.
- One service is a background worker that consumes SQS messages.

This gives you practical DevOps experience with realistic deployment patterns.

## Chosen beginner-friendly tools

| Area | Tool | Reason |
|---|---|---|
| Queue | AWS SQS | Easier than Kafka/MSK for the first project |
| Monitoring first | Prometheus + Grafana | Clear visibility into app and worker metrics |
| AWS monitoring later | CloudWatch | Best for SQS, RDS, EKS and AWS alarms |
| Tracing later | OpenTelemetry | Add after the system works |
| Worker autoscaling | KEDA | Scales workers based on queue depth |

## Why SQS first instead of Kafka/MSK?

Use SQS first because your goal is to learn deployment, workers, queues and autoscaling. Kafka/MSK introduces more operational complexity and can become a separate project later.

## Main learning outcomes

By the end of this project, you should understand:

- How to deploy API workloads and worker workloads separately.
- How to run database migrations before deployment.
- How to inject secrets through environment variables.
- How to use readiness and liveness probes properly.
- How to scale workers from queue depth.
- How to observe API latency, worker failures, queue depth and database connections.
- How to test rollback and failure scenarios.
