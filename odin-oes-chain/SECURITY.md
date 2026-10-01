# Security Policy

## Reporting a vulnerability

Do not disclose vulnerabilities in public issues. Report them privately to the ODIN ECOSYSTEM security contact distributed through the project's controlled communication channels. Include an impact summary, affected component, reproduction steps, and suggested mitigation where available.

Maintainers will acknowledge reports, assess severity, coordinate remediation, and publish disclosure information after affected operators have had a reasonable upgrade window.

## Security baseline

- Production secrets belong in an external secret manager, never in Git.
- Mainnet releases require reviewed, pinned dependencies and reproducible build evidence.
- Contracts require independent review and test coverage before deployment.
- Node RPC exposure, validator operations, and database access follow least-privilege network policies.
