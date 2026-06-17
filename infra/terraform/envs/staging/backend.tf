terraform {
  backend "s3" {
    bucket       = "REPLACE_WITH_EDFP_TERRAFORM_STATE_BUCKET"
    key          = "edfp/staging/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}
