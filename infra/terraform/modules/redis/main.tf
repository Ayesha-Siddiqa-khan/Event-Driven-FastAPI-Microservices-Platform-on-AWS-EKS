locals {
  name = "${var.project_name}-${var.environment}-redis-main"
  tags = merge(var.tags, {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  })
}

resource "aws_security_group" "this" {
  name        = "${local.name}-sg"
  description = "Allow Redis access from EKS workloads only"
  vpc_id      = var.vpc_id

  tags = merge(local.tags, { Name = "${local.name}-sg" })
}

resource "aws_vpc_security_group_ingress_rule" "redis" {
  for_each = toset(var.allowed_security_group_ids)

  security_group_id            = aws_security_group.this.id
  referenced_security_group_id = each.value
  from_port                    = 6379
  to_port                      = 6379
  ip_protocol                  = "tcp"
  description                  = "Redis from EKS"
}

resource "aws_vpc_security_group_egress_rule" "all" {
  security_group_id = aws_security_group.this.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_elasticache_subnet_group" "this" {
  name       = "${local.name}-subnets"
  subnet_ids = var.private_subnet_ids
}

resource "aws_elasticache_replication_group" "this" {
  replication_group_id       = local.name
  description                = "Redis cache for ${var.project_name} ${var.environment}"
  engine                     = "redis"
  engine_version             = var.engine_version
  node_type                  = var.node_type
  num_cache_clusters         = var.node_count
  automatic_failover_enabled = var.node_count > 1
  subnet_group_name          = aws_elasticache_subnet_group.this.name
  security_group_ids         = [aws_security_group.this.id]
  at_rest_encryption_enabled = true
  transit_encryption_enabled = false

  tags = merge(local.tags, { Name = local.name })
}
