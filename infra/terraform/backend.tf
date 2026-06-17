terraform {
  backend "local" {
    path = "state/dev/terraform.tfstate"
  }
}
