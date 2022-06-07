terraform {
  required_version = ">= 0.13.7" # ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 2"
    }
  }
}
