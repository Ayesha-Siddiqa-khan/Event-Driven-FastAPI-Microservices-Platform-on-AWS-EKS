# 08 - SQS Queues

SQS is the event backbone of this project.

## Why SQS

SQS decouples services. The order service does not need to wait for notifications. It can publish an event and continue.

## Queues to create

Use standard queues first:

```text
edfp-dev-order-events
edfp-dev-notification-events
```

## Queue purpose

| Queue | Producer | Consumer |
|---|---|---|
| `edfp-dev-order-events` | order-service | payment-service later, or manual/lab consumer |
| `edfp-dev-notification-events` | payment-service | notification-worker |

For the beginner version, the most important queue is `notification-events`, because the worker will consume from it.

## Queue URLs

Your apps need queue URLs, not only names.

Example format:

```text
https://sqs.us-east-1.amazonaws.com/<account-id>/edfp-dev-notification-events
```

Store queue URLs in Secrets Manager or inject them as environment variables.

## Environment variables

Order service:

```text
ORDER_EVENTS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/<account-id>/edfp-dev-order-events
AWS_REGION=us-east-1
```

Payment service:

```text
NOTIFICATION_EVENTS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/<account-id>/edfp-dev-notification-events
AWS_REGION=us-east-1
```

Notification worker:

```text
NOTIFICATION_EVENTS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/<account-id>/edfp-dev-notification-events
AWS_REGION=us-east-1
```

## Dead-letter queues

Add DLQs after the basic worker works.

Recommended names:

```text
edfp-dev-order-events-dlq
edfp-dev-notification-events-dlq
```

Recommended redrive setting:

```text
maxReceiveCount: 5
```

Meaning:

```text
If a message fails five times, move it to the dead-letter queue.
```

## IAM permissions

Order service needs:

```text
sqs:SendMessage
sqs:GetQueueAttributes
```

Payment service needs:

```text
sqs:SendMessage
sqs:GetQueueAttributes
```

Notification worker needs:

```text
sqs:ReceiveMessage
sqs:DeleteMessage
sqs:ChangeMessageVisibility
sqs:GetQueueAttributes
```

## KEDA autoscaling

Use KEDA to scale the notification worker based on SQS queue depth.

Beginner settings:

```text
min replicas: 1
max replicas: 5
queue length threshold: 5
```

Advanced settings:

```text
min replicas: 0
max replicas: 10
queue length threshold: 10
```

## Verification checklist

- queues exist
- apps receive queue URL through environment variables
- order-service can send test message
- payment-service can send notification message
- notification-worker can receive and delete message
- failed messages are not deleted
- DLQ receives repeatedly failing messages
- KEDA scales worker when queue depth increases
