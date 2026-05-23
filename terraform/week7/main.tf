# terraform/week7/main.tf

terraform {
  required_version = ">= 1.6"

  backend "gcs" {
    bucket = "lexical-sanctum-497121-q3-tfstate"
    prefix = "terraform/week7"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "networking" {
  source = "./modules/networking"

  project_id  = var.project_id
  region      = var.region
  vpc_name    = "cis410-vpc"
  subnet_cidr = "10.0.1.0/24"
  my_ip_cidr  = var.my_ip_cidr
}