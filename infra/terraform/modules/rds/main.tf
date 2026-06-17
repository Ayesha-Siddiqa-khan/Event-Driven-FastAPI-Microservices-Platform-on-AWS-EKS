locals {
  name = "${var.project_name}-${var.environment}-rds-postgres"
  tags = merge(var.tags, {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  })
}

resource "random_password" "db" {
  length           = 24
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_security_group" "this" {
  name        = "${local.name}-sg"
  description = "Allow PostgreSQL access from EKS workloads only"
  vpc_id      = var.vpc_id

  tags = merge(local.tags, { Name = "${local.name}-sg" })
}

resource "aws_vpc_security_group_ingress_rule" "postgres" {
  for_each = {
    for index, security_group_id in var.allowed_security_group_ids :
    tostring(index) => security_group_id
  }

  security_group_id            = aws_security_group.this.id
  referenced_security_group_id = each.value
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
  description                  = "PostgreSQL from EKS"
}

resource "aws_vpc_security_group_egress_rule" "all" {
  security_group_id = aws_security_group.this.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_db_subnet_group" "this" {
  name       = "${local.name}-subnets"
  subnet_ids = var.private_subnet_ids

  tags = merge(local.tags, { Name = "${local.name}-subnets" })
}

resource "aws_db_instance" "this" {
  identifier             = local.name
  engine                 = "postgres"
  engine_version         = var.engine_version
  instance_class         = var.instance_class
  allocated_storage      = var.allocated_storage
  db_name                = var.db_name
  username               = var.username
  password               = random_password.db.result
  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.this.id]
  publicly_accessible    = false
  multi_az               = var.multi_az
  storage_encrypted      = true
  deletion_protection    = var.deletion_protection
  skip_final_snapshot    = var.skip_final_snapshot

  tags = merge(local.tags, { Name = local.name })
}
