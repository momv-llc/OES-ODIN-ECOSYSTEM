# OES Chain

OES Chain is the planned EVM-compatible Layer 1 for the ODIN ECOSYSTEM. Its native asset is **OES**. This repository is the auditable foundation for the chain, Solidity contracts, operational infrastructure, explorer, and wallet clients.

> This initial repository deliberately contains **no blockchain application logic, mock transactions, synthetic RPC, or UI simulation**. Consensus, genesis, token economics, and release gates require separate approved ADRs and security review.

## Architecture

- **Consensus and application runtime:** Go, Cosmos SDK, CometBFT, and Cosmos EVM.
- **Execution compatibility:** Ethereum JSON-RPC and Solidity contracts through Cosmos EVM.
- **Data and clients:** PostgreSQL-backed explorer indexer boundary; React + TypeScript explorer and wallet workspaces.
- **Operations:** Docker Compose profiles, Prometheus, Grafana, and GitHub Actions.

See [architecture.md](docs/architecture.md) and [ADR-001](docs/ADR-001-stack.md).

## Environments

| Environment | Purpose | Safety rule |
| --- | --- | --- |
| `local` | isolated developer work | local-only state and credentials |
| `devnet` | integration validation | disposable network state |
| `testnet` | public pre-production validation | published genesis and monitored upgrades |
| `mainnet` | production network | change-controlled operations and external secret management |

Configuration is selected with `OES_ENV` and validates against `chain/config/environments.yaml`. Secrets are never committed; inject them using the deployment platform's secret store.

## Quick start

```bash
make check
make test
make docker-validate
```

These commands validate repository contracts only. They do not start a chain or publish an artifact.

## Repository layout

- `chain/` — future Go chain application boundary and environment policy.
- `contracts/` — Solidity source and test boundaries.
- `explorer/`, `wallet/` — React/TypeScript application boundaries.
- `infra/` — container, database, metrics, and dashboard provisioning.
- `docs/` — architecture decisions and operational documentation.
- `tests/` — repository-level validation tests.

## Governance and security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes and [SECURITY.md](SECURITY.md) before reporting a vulnerability.
