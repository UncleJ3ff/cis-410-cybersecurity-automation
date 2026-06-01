# Week 8: On-Premise Docker vs Cloud Run Comparison

## Comparison Table

| Dimension | On-Premise Docker (Wks 3–5) | Cloud Run (Week 8) |
|-----------|----------------------------|-------------------|
| Infrastructure setup | 3 VMs created, Docker installed on each | No servers to manage — just push an image and GCP handles provisioning |
| Deployment command | SSH → docker build → docker run | Single command: gcloud run deploy or terraform apply |
| TLS / HTTPS | Not configured — app ran on plain HTTP | Automatic HTTPS with no certificate management needed |
| Scaling approach | Manual — redeploy or add VMs | Automatic — scales up under load, scales to zero when idle |
| Port management | Ports 5000/5001/5002 per environment | No port management — Cloud Run handles routing automatically |
| Cost when idle | VM running 24/7 regardless of traffic | Zero cost when idle — scales to zero with no traffic |
| Rollback | Re-deploy previous image manually | Deploy previous image tag — revision history kept automatically |
| Secrets management | GitHub Secrets → env vars in workflow | GitHub Secrets → env vars in workflow (same approach) |

## Reflection Questions

### Q1: Which approach required more manual steps from push to live URL?

On-premise Docker required significantly more manual steps. For each deployment I had to SSH into the VM, build the Docker image on the machine, stop the old container, and start the new one. Cloud Run eliminated all of these steps — I push the image to Artifact Registry and run one deploy command. The steps eliminated were: SSH access, per-machine image builds, container lifecycle management, and port configuration.

### Q2: How do you know which version of code is running in production?

With on-premise Docker, it is difficult to know exactly which version is running without SSHing into the VM and checking the container. With Cloud Run and commit SHA tagging, every deployed image is tagged with the exact git commit (e.g., flask-app:2c14725). I can run git log and match the SHA to the exact line of code that is running in production, making audits and incident response much faster.

### Q3: What is the security advantage of scale-to-zero beyond cost savings?

When a service scales to zero there is no running process to attack. On-premise VMs run 24/7 meaning open ports, running processes, and potential vulnerabilities are exposed continuously. With scale-to-zero, the attack surface only exists when the service is actively handling requests. This reduces the window of exposure for any unpatched vulnerabilities in the container or its dependencies.

### Q4: What attack surface was eliminated by replacing SSH keys with OIDC?

SSH key secrets stored in GitHub Secrets are long-lived credentials — if stolen they grant permanent access until manually rotated. OIDC tokens are short-lived and scoped — they expire automatically and are tied to a specific workflow run. Eliminating SSH keys removed the risk of credential theft, key rotation failures, and unauthorized access through compromised secrets. There is no static credential to steal.
