
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.47.0"
    }
    null = {
      source = "hashicorp/null"
    }
    template = {
      source = "hashicorp/template"
    }
  }
  backend "s3" {
    region = "us-west-1"
  }
}

provider "null" {}

provider "aws" {
  region = "us-west-1"
}

