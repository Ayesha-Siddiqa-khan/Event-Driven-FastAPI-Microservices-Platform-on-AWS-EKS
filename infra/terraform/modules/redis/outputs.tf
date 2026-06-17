output "primary_endpoint_address" {
  value = aws_elasticache_replication_group.this.primary_endpoint_address
}

output "port" {
  value = local.port
}

output "redis_url" {
  value = "redis://${aws_elasticache_replication_group.this.primary_endpoint_address}:${local.port}/0"
}

output "security_group_id" {
  value = aws_security_group.this.id
}
