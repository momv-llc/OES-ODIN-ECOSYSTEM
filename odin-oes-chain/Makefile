SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

.PHONY: help fmt check test docker-validate tree

help: ## Show available validation commands.
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "%-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

fmt: ## Verify formatting of repository-owned text formats.
	@python3 scripts/validate_repository.py --format

check: ## Validate structure, environment separation, and forbidden production markers.
	@python3 scripts/validate_repository.py

test: ## Run repository baseline tests.
	@python3 -m unittest discover -s tests -v

docker-validate: ## Render Docker Compose configuration for each environment.
	@for environment in local devnet testnet mainnet; do \
		OES_ENV=$$environment docker compose -f infra/docker-compose.yml config --quiet; \
	done

tree: ## Print the intended top-level repository structure.
	@find . -maxdepth 2 -type d | sort
