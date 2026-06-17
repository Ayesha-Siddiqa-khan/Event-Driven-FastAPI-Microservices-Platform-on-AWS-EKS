# 07 - Failure Labs

Use these labs for portfolio screenshots and README proof.

## Failure Lab 1 - Kill API pod

Action:

```text
Delete an api-gateway pod.
```

Expected result:

```text
Kubernetes creates a replacement pod.
Service remains available.
```

## Failure Lab 2 - Break readiness

Action:

```text
Set wrong Redis URL for order-service.
```

Expected result:

```text
/ready fails.
Kubernetes removes pod from service endpoints.
Traffic should not go to unready pod.
```

## Failure Lab 3 - Bad release rollback

Action:

```text
Deploy an image where POST /orders returns HTTP 500.
```

Expected result:

```text
Smoke test fails.
GitHub Actions triggers Helm rollback.
Old version is restored.
```

## Failure Lab 4 - Queue depth scaling

Action:

```text
Send 500 messages to notification-events-queue.
```

Expected result:

```text
KEDA scales notification-worker replicas up.
Queue depth decreases.
KEDA scales worker down later.
```

## Failure Lab 5 - Database failure

Action:

```text
Use wrong DATABASE_URL or block DB access.
```

Expected result:

```text
/ready fails.
Migration job fails.
Deployment should stop.
```

## Failure Lab 6 - Load test

Action:

```text
Run k6 against api-gateway.
```

Expected result:

```text
HPA scales API pods.
Grafana shows increased latency, request rate and CPU.
```
