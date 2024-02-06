terraform {
    required_providers {
      aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
      }
    }
}

provider "aws" {
    region = "us-east-2"
}


module "get_league_entries_lambda" {
    source = "./lambdas/get_league_entries"
}
