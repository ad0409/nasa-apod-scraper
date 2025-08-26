---
applyTo: "**/k8s/**/*.yaml"
---

- Include resource requests and limits for every pod/container.
- Define liveness and readiness probes.
- Use labels: `app`, `env`, `version` consistently.
- Prefer ConfigMaps/Secrets over inline configuration.
- Apply GitOps principles: manifests should be declarative and idempotent.
