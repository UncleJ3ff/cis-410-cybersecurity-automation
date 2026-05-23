# terraform/week7/modules/networking/main.tf

resource "google_compute_network" "vpc" {
  name                    = var.vpc_name
  auto_create_subnetworks = false
  project                 = var.project_id
}

resource "google_compute_subnetwork" "public" {
  name          = "${var.vpc_name}-public"
  ip_cidr_range = var.subnet_cidr
  region        = var.region
  network       = google_compute_network.vpc.id
  project       = var.project_id
}

resource "google_compute_firewall" "allow_ssh" {
  name    = "${var.vpc_name}-allow-ssh"
  network = google_compute_network.vpc.name
  project = var.project_id

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = [var.my_ip_cidr]
  target_tags   = ["ssh-enabled"]
  description   = "Allow SSH from operator IP only"
}

resource "google_compute_firewall" "allow_http" {
  name    = "${var.vpc_name}-allow-http"
  network = google_compute_network.vpc.name
  project = var.project_id

  allow {
    protocol = "tcp"
    ports    = ["80", "8080"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["web-server"]
  description   = "Allow HTTP traffic to web-tagged resources"
}

resource "google_compute_firewall" "deny_all_ingress" {
  name      = "${var.vpc_name}-deny-ingress"
  network   = google_compute_network.vpc.name
  project   = var.project_id
  priority  = 65000
  direction = "INGRESS"

  deny { protocol = "all" }

  source_ranges = ["0.0.0.0/0"]
  description   = "Explicit deny-all fallback"
}