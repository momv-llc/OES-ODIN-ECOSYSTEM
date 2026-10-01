# ADR-001: OES Chain foundation stack

- **Status:** Accepted
- **Date:** 2026-10-01
- **Decision owners:** ODIN ECOSYSTEM architecture

## Context

OES Chain requires a production-oriented, EVM-compatible L1 foundation while retaining the Cosmos ecosystem's application and consensus model. The repository must select versions that are explicitly compatible, rather than independently choosing newest major releases.

## Decision

Use the following pinned foundation matrix for the first implementation milestone:

| Component | Selected version | Compatibility evidence |
| --- | --- | --- |
| Go | 1.25.9 | Required by Cosmos EVM `v0.7.3` module metadata. |
| Cosmos EVM | `v0.7.3` | Security patch release; module pins the application stack below. |
| Cosmos SDK | `v0.54.3` | Direct dependency in Cosmos EVM `v0.7.3`. |
| CometBFT | `v0.39.3` | Direct dependency in Cosmos EVM `v0.7.3`. |
| go-ethereum | `v1.16.8` | Direct dependency used by Cosmos EVM `v0.7.3`. |
| Solidity | 0.8.30 | Compiler line for future contracts; pin exact compiler in the contract workspace before deployment. |
| PostgreSQL | 17 | Supported operational datastore baseline for off-chain indexing. |
| React | 19 | Client baseline, pinned in each future workspace lockfile. |
| TypeScript | 5.9 | Client baseline, pinned in each future workspace lockfile. |

The chain implementation must import Cosmos EVM at `v0.7.3` and allow its Go module graph to retain the declared Cosmos SDK and CometBFT versions. Direct upgrades of either transitive foundation component require a replacement ADR plus compatibility and upgrade testing.

## Compatibility verification

The `v0.7.3` Cosmos EVM release's `go.mod` directly requires `github.com/cosmos/cosmos-sdk v0.54.3` and `github.com/cometbft/cometbft v0.39.3`; this is the authoritative compatibility constraint used here. It also requires Go `1.25.9` and go-ethereum `v1.16.8`. The selection avoids mixing Cosmos SDK `v0.55.0` or CometBFT `v0.40.0` with Cosmos EVM `v0.7.3`, because those newer releases are not its declared dependency pair.

Version verification was performed on 2026-10-01 against the Cosmos EVM `v0.7.3` release tag and module manifest. Cosmos EVM `v0.7.3` release notes identify important security fixes and a state-breaking upgrade, so an eventual adoption requires coordinated governance and a migration plan.

## Consequences

- The first chain implementation has a known, reproducible dependency graph.
- Upgrade work must be deliberate and tested across state migration, RPC behavior, consensus, and contract compatibility.
- No consensus or transaction logic is implemented by this ADR or this repository baseline.

## Sources

- Cosmos EVM release: <https://github.com/cosmos/evm/releases/tag/v0.7.3>
- Cosmos EVM module manifest: <https://raw.githubusercontent.com/cosmos/evm/v0.7.3/go.mod>
- Cosmos SDK releases: <https://github.com/cosmos/cosmos-sdk/releases>
- CometBFT releases: <https://github.com/cometbft/cometbft/releases>
