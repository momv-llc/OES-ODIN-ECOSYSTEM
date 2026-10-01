# OES Devnet

`docker-compose.devnet.yml` initializes three independent CometBFT homes, produces three gentxs, collects one shared genesis, compares its SHA-256 across all homes, and configures persistent peer IDs before nodes start.

Use `make devnet` to start the network and `make smoke-test` to verify consensus plus a native `100 OES` (`100000000000000000000uoes`) transfer. Use `make devnet-down` to remove devnet state.
