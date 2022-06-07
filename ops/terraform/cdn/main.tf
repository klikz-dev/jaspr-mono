terraform {
  backend "s3" {
    region = "us-west-1"
  }

}

provider "aws" {
  region  = "us-east-1"
  version = "~> 3"
}
