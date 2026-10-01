# Contributing to OES Chain

## Scope

This repository establishes interfaces and operational guardrails. Do not add consensus logic, chain IDs, genesis allocations, validators, keys, or deployable contracts without an approved ADR and review by maintainers.

## Workflow

1. Create a focused branch and document architecture-impacting decisions in `docs/`.
2. Run `make fmt`, `make check`, and `make test` locally.
3. Keep local, devnet, testnet, and mainnet configuration separate.
4. Never commit credentials, mnemonic phrases, private keys, or production endpoints.
5. Request security review for changes affecting signing, RPC, genesis, networking, or infrastructure.

## Commit conventions

Use an imperative subject line such as `docs: define OES stack decision`. Keep commits independently reviewable.
