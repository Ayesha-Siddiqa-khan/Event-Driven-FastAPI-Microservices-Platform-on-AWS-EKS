output "endpoint" {
  value = aws_db_instance.this.address
}

output "port" {
  value = aws_db_instance.this.port
}

output "username" {
  value = var.username
}

output "password" {
  value     = random_password.db.result
  sensitive = true
}

output "database_url" {
  value     = "postgresql://${var.username}:${urlencode(random_password.db.result)}@${aws_db_instance.this.address}:${aws_db_instance.this.port}/${var.db_name}"
  sensitive = true
}

output "security_group_id" {
  value = aws_security_group.this.id
}
