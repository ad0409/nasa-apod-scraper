# Copilot Instructions – Baseline

This document provides the primary instructions for GitHub Copilot when working with this codebase. These rules apply repository-wide unless overridden by more specific instructions.

## File Pattern Instructions

| Pattern | File Path | Description |
| ------- | --------- | ----------- |
| `.github/workflows/*.yml` | `.github/instructions/ci-cd.instructions.md` | CI/CD workflow configurations |
| `**/k8s/**/*.yaml` | `.github/instructions/kubernetes.instructions.md` | Kubernetes manifest files |
| `**/scripts/**/*.py` | `.github/instructions/python-scripts.instructions.md` | Python scripts and applications |
| `**/terraform/**/*.tf` | `.github/instructions/terraform.instructions.md` | Terraform infrastructure code |

## General
- Write clean, maintainable, production-ready code
- Use explicit, idiomatic solutions (Pythonic for Python, POSIX-compliant for Bash, YAML best practices)
- Add comments where intent is not obvious
- Explain design decisions briefly before showing code
- Prefer clarity over cleverness
- Include appropriate comments and documentation
- Follow language-specific style guides
- Use always the English language for code
- If the chat language is German, use a direct, professional, friendly tone and wording 

## Security
- Never commit sensitive information
- Never expose secrets, credentials, or tokens in code/configs
- Use environment variables for secrets
- Never hardcode secrets; use environment variables or secret managers
- Follow principle of least privilege
- Apply least privilege in IAM/RBAC and CI/CD
- Sanitize inputs and validate user data

## Infrastructure & DevOps
- Infrastructure-as-Code must be idempotent and reproducible
- Docker:
  - Use slim, version-pinned base images
  - Prefer multi-stage builds
  - Each container should have a single responsibility
- Kubernetes:
  - Always define resource requests/limits
  - Include liveness and readiness probes
  - Use consistent labels/annotations
- CI/CD:
  - Pipelines must include linting, testing, and security scans
  - Fail early with clear, visible errors

## Python
- Follow PEP8 and PEP20.
- Use type hints and docstrings.
- Format with black, lint with ruff (or flake8/pylint).
- Testing with pytest, prefer fixtures.
- Handle exceptions explicitly (no blanket `except Exception`).
- Dependencies managed with Poetry or pip-tools.

## Documentation & Output
- Every script/module must include short usage docs or examples
- Provide file structure when multiple files are involved
- Show full, clean implementations by default
- Update relevant documentation
- Include clear usage examples
- Document dependencies and requirements

## Testing
- Include tests for new functionality
- Ensure existing tests pass
- Document test coverage requirements
- Testing with pytest for Python, prefer fixtures
## Testing
- Include tests for new functionality
- Ensure existing tests pass
- Document test coverage requirements
- Testing with pytest for Python, prefer fixtures

## Reference Documentation

For specific guidelines, refer to the instruction files in `.github/instructions/`.
