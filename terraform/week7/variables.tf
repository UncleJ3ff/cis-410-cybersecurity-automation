variable "project_id" {
  description = "Your GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "my_ip_cidr" {
  description = "Your public IP for SSH access (format: x.x.x.x/32)"
  type        = string
}
