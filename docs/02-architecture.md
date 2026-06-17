# 02 - Architecture

## Services

```text
Client
  ↓
api-gateway
  ↓
  ├── auth-service ───── PostgreSQL + Redis
  ├── order-service ──── PostgreSQL + Redis + SQS order-events-queue
  └── payment-service ── PostgreSQL + SQS notification-events-queue
                                      ↓
                              notification-worker
                                      ↓
                                  PostgreSQL
```

## Application flow

```text
1. User registers through api-gateway.
2. api-gateway forwards to auth-service.
3. User creates an order through api-gateway.
4. api-gateway forwards to order-service.
5. order-service saves the order in PostgreSQL.
6. order-service caches the order in Redis.
7. order-service publishes an order_created message to SQS.
8. User triggers payment through api-gateway.
9. payment-service saves payment in PostgreSQL.
10. payment-service publishes a payment_completed message to SQS.
11. notification-worker consumes payment messages.
12. notification-worker saves notification records in PostgreSQL.
```

## Queues

Use two SQS standard queues:

```text
order-events-queue
notification-events-queue
```

### order-events-queue message

```json
{
  "event_type": "order_created",
  "order_id": "1",
  "user_id": "5",
  "amount": 100
}
```

### notification-events-queue message

```json
{
  "event_type": "payment_completed",
  "order_id": "1",
  "payment_id": "10",
  "user_id": "5",
  "status": "success"
}
```

## Deployment idea

API services should have:

- Kubernetes Deployment
- Kubernetes Service
- Ingress only for `api-gateway`
- liveness probe
- readiness probe
- HorizontalPodAutoscaler

Worker service should have:

- Kubernetes Deployment
- no public Ingress
- KEDA ScaledObject
- liveness probe
- readiness probe
- graceful shutdown
