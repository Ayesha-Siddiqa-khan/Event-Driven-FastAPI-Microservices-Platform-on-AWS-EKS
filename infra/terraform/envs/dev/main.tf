terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

data "aws_caller_identity" "current" {}

locals {
  namespace = "${var.project_name}-${var.environment}"
  services = [
    "api-gateway",
    "auth-service",
    "order-service",
    "payment-service",
    "notification-worker",
  ]
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

module "vpc" {
  source = "../../modules/vpc"

  project_name         = var.project_name
  environment          = var.environment
  vpc_cidr             = var.vpc_cidr
  azs                  = var.azs
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  single_nat_gateway   = var.single_nat_gateway
  tags                 = local.common_tags
}

module "eks" {
  source = "../../modules/eks"

  project_name        = var.project_name
  environment         = var.environment
  cluster_version     = var.eks_cluster_version
  private_subnet_ids  = module.vpc.private_subnet_ids
  node_instance_types = var.eks_node_instance_types
  node_desired_size   = var.eks_node_desired_size
  node_min_size       = var.eks_node_min_size
  node_max_size       = var.eks_node_max_size
  tags                = local.common_tags
}

module "ecr" {
  source = "../../modules/ecr"

  project_name = var.project_name
  environment  = var.environment
  repositories = local.services
  tags         = local.common_tags
}

module "rds" {
  source = "../../modules/rds"

  project_name               = var.project_name
  environment                = var.environment
  vpc_id                     = module.vpc.vpc_id
  private_subnet_ids         = module.vpc.private_subnet_ids
  allowed_security_group_ids = [module.eks.cluster_security_group_id]
  instance_class             = var.rds_instance_class
  allocated_storage          = var.rds_allocated_storage
  multi_az                   = var.rds_multi_az
  deletion_protection        = var.environment == "prod"
  skip_final_snapshot        = var.environment != "prod"
  tags                       = local.common_tags
}

module "redis" {
  source = "../../modules/redis"

  project_name               = var.project_name
  environment                = var.environment
  vpc_id                     = module.vpc.vpc_id
  private_subnet_ids         = module.vpc.private_subnet_ids
  allowed_security_group_ids = [module.eks.cluster_security_group_id]
  node_type                  = var.redis_node_type
  node_count                 = var.redis_node_count
  tags                       = local.common_tags
}

module "sqs" {
  source = "../../modules/sqs"

  project_name = var.project_name
  environment  = var.environment
  tags         = local.common_tags
}

module "secrets" {
  source = "../../modules/secrets-manager"

  project_name = var.project_name
  environment  = var.environment
  secret_values = {
    "/${var.project_name}/${var.environment}/auth-service/database-url"                         = module.rds.database_url
    "/${var.project_name}/${var.environment}/auth-service/redis-url"                            = module.redis.redis_url
    "/${var.project_name}/${var.environment}/order-service/database-url"                        = module.rds.database_url
    "/${var.project_name}/${var.environment}/order-service/redis-url"                           = module.redis.redis_url
    "/${var.project_name}/${var.environment}/order-service/order-events-queue-url"              = module.sqs.order_events_queue_url
    "/${var.project_name}/${var.environment}/payment-service/database-url"                      = module.rds.database_url
    "/${var.project_name}/${var.environment}/payment-service/notification-events-queue-url"     = module.sqs.notification_events_queue_url
    "/${var.project_name}/${var.environment}/notification-worker/database-url"                  = module.rds.database_url
    "/${var.project_name}/${var.environment}/notification-worker/notification-events-queue-url" = module.sqs.notification_events_queue_url
    "/${var.project_name}/${var.environment}/api-gateway/auth-service-url"                      = "http://${var.project_name}-${var.environment}-auth-service:8000"
    "/${var.project_name}/${var.environment}/api-gateway/order-service-url"                     = "http://${var.project_name}-${var.environment}-order-service:8000"
    "/${var.project_name}/${var.environment}/api-gateway/payment-service-url"                   = "http://${var.project_name}-${var.environment}-payment-service:8000"
  }
  tags = local.common_tags
}

module "github_oidc" {
  source = "../../modules/iam-github-oidc"

  project_name  = var.project_name
  environment   = var.environment
  github_org    = var.github_org
  github_repo   = var.github_repo
  github_branch = var.github_branch
  tags          = local.common_tags
}

module "irsa" {
  source = "../../modules/iam-irsa"

  project_name                  = var.project_name
  environment                   = var.environment
  namespace                     = local.namespace
  oidc_provider_arn             = module.eks.oidc_provider_arn
  oidc_provider_url             = module.eks.oidc_provider_url
  order_events_queue_arn        = module.sqs.order_events_queue_arn
  notification_events_queue_arn = module.sqs.notification_events_queue_arn
  secret_arns                   = values(module.secrets.secret_arns)
  tags                          = local.common_tags
}

module "monitoring" {
  source = "../../modules/monitoring"

  project_name = var.project_name
  environment  = var.environment
  tags         = local.common_tags
}
