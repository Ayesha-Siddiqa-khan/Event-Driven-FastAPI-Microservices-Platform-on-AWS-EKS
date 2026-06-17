locals {
  tags = merge(var.tags, {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  })
}

resource "aws_sqs_queue" "order_events_dlq" {
  name                      = "${var.project_name}-${var.environment}-order-events-dlq"
  message_retention_seconds = var.message_retention_seconds
  tags                      = merge(local.tags, { Name = "${var.project_name}-${var.environment}-order-events-dlq" })
}

resource "aws_sqs_queue" "notification_events_dlq" {
  name                      = "${var.project_name}-${var.environment}-notification-events-dlq"
  message_retention_seconds = var.message_retention_seconds
  tags                      = merge(local.tags, { Name = "${var.project_name}-${var.environment}-notification-events-dlq" })
}

resource "aws_sqs_queue" "order_events" {
  name                       = "${var.project_name}-${var.environment}-order-events"
  visibility_timeout_seconds = var.visibility_timeout_seconds
  message_retention_seconds  = var.message_retention_seconds

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.order_events_dlq.arn
    maxReceiveCount     = var.max_receive_count
  })

  tags = merge(local.tags, { Name = "${var.project_name}-${var.environment}-order-events" })
}

resource "aws_sqs_queue" "notification_events" {
  name                       = "${var.project_name}-${var.environment}-notification-events"
  visibility_timeout_seconds = var.visibility_timeout_seconds
  message_retention_seconds  = var.message_retention_seconds

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.notification_events_dlq.arn
    maxReceiveCount     = var.max_receive_count
  })

  tags = merge(local.tags, { Name = "${var.project_name}-${var.environment}-notification-events" })
}
