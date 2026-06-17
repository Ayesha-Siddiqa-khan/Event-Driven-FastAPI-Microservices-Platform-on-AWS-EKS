# 06 - Monitoring and Alerting

## First monitoring stack

Use:

```text
Prometheus + Grafana
```

Add CloudWatch after Prometheus works.

## Metrics exposed by services

Common HTTP metrics are exposed through `/metrics`.

Recommended dashboard panels:

```text
API request rate
API p95 latency
API 4xx and 5xx errors
worker processed messages
worker failed messages
SQS queue depth
pod restarts
CPU usage
memory usage
database readiness failures
Redis readiness failures
```

## App-level custom metrics

Examples:

```text
user_registrations_total
user_logins_total
orders_created_total
sqs_messages_published_total
sqs_publish_failures_total
payments_created_total
worker_messages_processed_total
worker_messages_failed_total
```

## CloudWatch phase

Add CloudWatch later for:

```text
SQS ApproximateNumberOfMessagesVisible
RDS CPUUtilization
RDS DatabaseConnections
ElastiCache CPU/Memory
EKS logs
ALB target response time
ALB 5xx errors
```

## OpenTelemetry phase

Add OpenTelemetry only after the project is stable.

Tracing goal:

```text
api-gateway -> order-service -> SQS -> payment-service -> notification-worker
```
