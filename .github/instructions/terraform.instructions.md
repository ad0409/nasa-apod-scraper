---
applyTo: "**/terraform/**/*.tf"
---

- Write Terraform code using modules, avoid duplication.
- Pin provider versions explicitly.
- Variables and secrets must come from `.tfvars` or environment, never hardcoded.
- Use `terraform fmt` and `terraform validate`.
- Ensure resources are tagged/labeled consistently.
