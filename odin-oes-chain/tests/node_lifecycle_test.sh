#!/usr/bin/env bash
set -euo pipefail

binary=${1:?path to oesd is required}
home=$(mktemp -d)
trap 'rm -rf "$home"' EXIT

"$binary" init validator --chain-id oes-local-1 --home "$home" >/dev/null
"$binary" validate-genesis --home "$home" >/dev/null
"$binary" keys add operator --keyring-backend test --home "$home" >/dev/null
"$binary" keys list --keyring-backend test --home "$home" >/dev/null
"$binary" query bank params --home "$home" --offline >/dev/null
python3 - "$home/config/genesis.json" <<'PY'
import json
import sys

genesis = json.load(open(sys.argv[1], encoding="utf-8"))
assert genesis["chain_id"] == "oes-local-1"
evm = genesis["app_state"]["evm"]["params"]
assert evm["evm_denom"] == "uoes"
PY
