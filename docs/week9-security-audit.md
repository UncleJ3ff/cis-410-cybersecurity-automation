# Week 9 Security Audit

## IAM Permissions Audit
| Service | Before (Over-permissioned) | After (Least-privilege) |
| :--- | :--- | :--- |
| **Cloud Run** | `roles/run.admin` | `roles/run.developer` |
| **Cloud Storage** | `roles/storage.admin` (Project-wide) | `roles/storage.admin` (tfstate Bucket only) |

## Reflection Questions

**1. Why do we use Google Secret Manager instead of GitHub Secrets?**
*Your answer here (Hint: Secret manager lets the app pull passwords at runtime and gives you a full audit log!)*

**2. What does severity>=WARNING do in a logging alert?**
*Your answer here (Hint: It only alerts you on actual errors, ignoring regular informational traffic logs).*

**3. Why is it important to set up a billing budget alert?**
*Your answer here (Hint: So you get an email before getting a massive surprise bill!)*
