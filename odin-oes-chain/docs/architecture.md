# OES Chain architecture

## System boundaries

```text
Wallet (React/TypeScript) ── Ethereum JSON-RPC ──> OES Chain node
Explorer (React/TypeScript) ── indexer boundary ──> PostgreSQL
                                                └─> OES Chain RPC
Solidity contracts ── deployment tooling ────────> OES Chain EVM
Prometheus ── scrape ──> node / operational services ──> Grafana
```

The future chain application is the only authoritative source of chain state. PostgreSQL is an off-chain derived-data store for explorer use and is never a consensus dependency. Wallet and explorer applications must treat RPC data as untrusted transport input and rely on chain verification rules.

## Trust and deployment model

- Validator keys, signing infrastructure, and operational secrets remain outside this repository.
- Environment configuration expresses policy only; live endpoints, credentials, genesis material, and private topology are deployed through controlled release systems.
- `local` and `devnet` may use disposable state. `testnet` and `mainnet` require reviewed releases, observability, rollback planning, and change control.
- Metrics are exposed only within the deployment network or behind authenticated access controls.

## Future implementation gates

Before application logic begins, approve ADRs for token denomination and display units, chain identifiers, genesis process, validator onboarding, upgrade process, RPC exposure, gas policy, IBC posture, and key management.
