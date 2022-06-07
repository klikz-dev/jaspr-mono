
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.47.0"
    }
  }
  backend "s3" {
    region = "us-west-1"
  }
}

provider "aws" {
  region  = "us-east-1"
}
