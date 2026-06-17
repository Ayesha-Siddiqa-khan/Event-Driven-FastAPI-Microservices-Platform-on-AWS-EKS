variable "project_name" {
  type    = string
  default = "edfp"
}

variable "environment" {
  type    = string
  default = "staging"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "github_org" {
  type = string
}

variable "github_repo" {
  type = string
}

variable "github_branch" {
  type    = string
  default = "main"
}

variable "vpc_cidr" {
  type    = string
  default = "10.30.0.0/16"
}

variable "azs" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b"]
}

variable "public_subnet_cidrs" {
  type    = list(string)
  default = ["10.30.0.0/24", "10.30.1.0/24"]
}

variable "private_subnet_cidrs" {
  type    = list(string)
  default = ["10.30.10.0/24", "10.30.11.0/24"]
}

variable "single_nat_gateway" {
  type    = bool
  default = true
}

variable "eks_cluster_version" {
  type    = string
  default = "1.31"
}

variable "eks_node_instance_types" {
  type    = list(string)
  default = ["t3.medium"]
}

variable "eks_node_desired_size" {
  type    = number
  default = 2
}

variable "eks_node_min_size" {
  type    = number
  default = 2
}

variable "eks_node_max_size" {
  type    = number
  default = 4
}

variable "rds_instance_class" {
  type    = string
  default = "db.t4g.micro"
}

variable "rds_allocated_storage" {
  type    = number
  default = 30
}

variable "rds_multi_az" {
  type    = bool
  default = false
}

variable "redis_node_type" {
  type    = string
  default = "cache.t4g.micro"
}

variable "redis_node_count" {
  type    = number
  default = 1
}
