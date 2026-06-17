locals {
  name = "/aws/eks/${var.project_name}-${var.environment}-eks/application"
  tags = merge(var.tags, {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  })
}

resource "aws_cloudwatch_log_group" "application" {
  name              = local.name
  retention_in_days = var.retention_in_days

  tags = merge(local.tags, { Name = local.name })
}
