variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region for the subnet"
  type        = string
  default     = "us-central1"
}

variable "vpc_name" {
  description = "Name prefix for the VPC and all resources"
  type        = string
}

variable "subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
}

variable "my_ip_cidr" {
  description = "Your public IP for SSH access"
  type        = string
}
