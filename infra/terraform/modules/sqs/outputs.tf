output "order_events_queue_url" {
  value = aws_sqs_queue.order_events.url
}

output "order_events_queue_arn" {
  value = aws_sqs_queue.order_events.arn
}

output "notification_events_queue_url" {
  value = aws_sqs_queue.notification_events.url
}

output "notification_events_queue_arn" {
  value = aws_sqs_queue.notification_events.arn
}

output "notification_events_dlq_arn" {
  value = aws_sqs_queue.notification_events_dlq.arn
}
