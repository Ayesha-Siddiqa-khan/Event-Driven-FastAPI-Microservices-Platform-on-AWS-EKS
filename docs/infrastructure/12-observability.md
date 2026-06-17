# 12 - Observability: Prometheus, Grafana, CloudWatch, Logs, and Alerts

Build observability in phases.

## Phase 1: Prometheus and Grafana

Use Prometheus and Grafana first because they are easier for learning application metrics.

Your apps expose:

```text
/metrics
```

Prometheus scrapes metrics from:

```text
api-gateway
auth-service
order-service
payment-service
notification-worker
```

Grafana shows dashboards.

## Application metrics to watch

| Metric | Why it matters |
|---|---|
| request count | shows traffic |
| request latency | shows slowness |
| HTTP 5xx errors | shows broken releases |
| worker processed messages | shows worker is alive |
| worker failed messages | shows processing issues |
| SQS messages published | shows event flow |
| database readiness failures | shows database dependency issue |
| Redis readiness failures | shows cache/session issue |

## Phase 2: AWS CloudWatch

Add CloudWatch after Prometheus works.

Use CloudWatch for:

```text
EKS node/pod infrastructure metrics
CloudWatch logs
SQS queue metrics
RDS CPU, storage, connections
ElastiCache CPU, memory, connections
ALB target health and 5xx errors
```

## Recommended CloudWatch log groups

```text
/aws/eks/edfp-dev/app/api-gateway
/aws/eks/edfp-dev/app/auth-service
/aws/eks/edfp-dev/app/order-service
/aws/eks/edfp-dev/app/payment-service
/aws/eks/edfp-dev/app/notification-worker
```

## Recommended alarms

| Alarm | Condition example |
|---|---|
| API high 5xx | 5xx rate above threshold |
| API high latency | p95 latency too high |
| SQS queue backlog | visible messages above threshold |
| DLQ has messages | any visible message in DLQ |
| RDS high CPU | CPU above threshold |
| RDS connection pressure | connections too high |
| Redis high memory | memory above threshold |
| Pod restarts | restart count increases |

## Phase 3: OpenTelemetry

Add OpenTelemetry later to trace requests across services.

Trace example:

```text
api-gateway
↓
order-service
↓
SQS
↓
payment-service
↓
notification-worker
```

Do not start with OpenTelemetry. Add it after deployments, monitoring, rollback, and autoscaling are working.

## Verification checklist

- every service exposes `/metrics`
- Prometheus can scrape each service
- Grafana dashboard shows request rate and latency
- SQS queue depth is visible
- worker processed/failed message metrics are visible
- CloudWatch logs contain structured JSON logs
- alarms trigger during failure labs
