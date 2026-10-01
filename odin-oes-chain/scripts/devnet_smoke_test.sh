#!/usr/bin/env bash
set -euo pipefail
compose=(docker compose -f docker-compose.devnet.yml)
exec_node() { "${compose[@]}" exec -T validator-1 "$@"; }
for attempt in $(seq 1 60); do
  height=$(curl -fsS http://127.0.0.1:26657/status | jq -r '.result.sync_info.latest_block_height' || true)
  if [ "${height:-0}" -ge 2 ]; then break; fi
  sleep 2
done
[ "${height:-0}" -ge 2 ] || { echo "consensus did not produce blocks" >&2; exit 1; }
for node in validator-1 validator-2 validator-3; do
  other=$("${compose[@]}" exec -T "$node" curl -fsS http://127.0.0.1:26657/status | jq -r '.result.sync_info.latest_block_height')
  [ "$other" -ge 2 ] || { echo "$node is not synchronized" >&2; exit 1; }
done
exec_node oesd keys add wallet-a --keyring-backend test --home /root/.oesd >/dev/null
exec_node oesd keys add wallet-b --keyring-backend test --home /root/.oesd >/dev/null
sender=$(exec_node oesd keys show validator-1 -a --keyring-backend test --home /root/.oesd)
wallet_a=$(exec_node oesd keys show wallet-a -a --keyring-backend test --home /root/.oesd)
wallet_b=$(exec_node oesd keys show wallet-b -a --keyring-backend test --home /root/.oesd)
exec_node oesd tx bank send "$sender" "$wallet_a" 200000000000000000000uoes --chain-id oes-devnet-1 --keyring-backend test --home /root/.oesd --yes --broadcast-mode block >/dev/null
exec_node oesd tx bank send "$wallet_a" "$wallet_b" 100000000000000000000uoes --chain-id oes-devnet-1 --keyring-backend test --home /root/.oesd --yes --broadcast-mode block >/dev/null
balance=$(exec_node oesd query bank balances "$wallet_b" --home /root/.oesd -o json | jq -r '.balances[] | select(.denom == "uoes") | .amount')
[ "$balance" = "100000000000000000000" ] || { echo "unexpected wallet B balance: $balance" >&2; exit 1; }
echo "OES devnet smoke test passed at height $height"
