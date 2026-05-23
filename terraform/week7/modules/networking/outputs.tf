output "vpc_name" { value = google_compute_network.vpc.name }
output "vpc_id" { value = google_compute_network.vpc.self_link }
output "subnet_name" { value = google_compute_subnetwork.public.name }
output "subnet_cidr" { value = google_compute_subnetwork.public.ip_cidr_range }
