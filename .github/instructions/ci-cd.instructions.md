---
applyTo: ".github/workflows/*.yml"
---

- Workflows must include: checkout, lint, test, build, deploy.
- Cache dependencies (pip, npm, terraform) for faster runs.
- Fail early; surface errors clearly.
- No secrets in workflows; use GitHub Secrets or OIDC.
- Use matrix builds for multi-version testing (e.g. Python 3.10–3.12).
