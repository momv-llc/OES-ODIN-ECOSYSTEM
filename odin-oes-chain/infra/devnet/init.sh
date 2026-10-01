#!/usr/bin/env bash
set -euo pipefail

if [ -f /shared/ready ]; then exit 0; fi
CHAIN_ID=${OES_DEVNET_CHAIN_ID:-oes-devnet-1}
DENOM=uoes
STAKE=1000000000000000000000000
for n in 1 2 3; do
  home=/validator${n}
  oesd init "validator-${n}" --chain-id "$CHAIN_ID" --home "$home" >/dev/null
  oesd keys add "validator-${n}" --keyring-backend test --home "$home" >/dev/null
  address=$(oesd keys show "validator-${n}" -a --keyring-backend test --home "$home")
  echo "$address" > "/shared/validator-${n}.address"
  oesd add-genesis-account "$address" "${STAKE}${DENOM}" --home "$home"
done
# Build genesis once and distribute it identically to every node.
for n in 1 2 3; do
  home=/validator${n}
  if [ "$n" != 1 ]; then cp /validator1/config/genesis.json "$home/config/genesis.json"; fi
  oesd gentx "validator-${n}" "100000000000000000000000${DENOM}" --chain-id "$CHAIN_ID" --keyring-backend test --home "$home"
done
cp /validator2/config/gentx/* /validator1/config/gentx/
cp /validator3/config/gentx/* /validator1/config/gentx/
oesd collect-gentxs --home /validator1 >/dev/null
for n in 2 3; do cp /validator1/config/genesis.json /validator${n}/config/genesis.json; done
hash=$(sha256sum /validator1/config/genesis.json | awk '{print $1}')
printf '%s\n' "$hash" > /shared/genesis.sha256
for n in 1 2 3; do
  test "$(sha256sum /validator${n}/config/genesis.json | awk '{print $1}')" = "$hash"
  id=$(oesd comet show-node-id --home /validator${n})
  echo "$id" > "/shared/validator-${n}.nodeid"
done
peers="$(cat /shared/validator-2.nodeid)@validator-2:26656,$(cat /shared/validator-3.nodeid)@validator-3:26656"
sed -i "s|^persistent_peers = .*|persistent_peers = \"${peers}\"|" /validator1/config/config.toml
peers="$(cat /shared/validator-1.nodeid)@validator-1:26656,$(cat /shared/validator-3.nodeid)@validator-3:26656"
sed -i "s|^persistent_peers = .*|persistent_peers = \"${peers}\"|" /validator2/config/config.toml
peers="$(cat /shared/validator-1.nodeid)@validator-1:26656,$(cat /shared/validator-2.nodeid)@validator-2:26656"
sed -i "s|^persistent_peers = .*|persistent_peers = \"${peers}\"|" /validator3/config/config.toml
touch /shared/ready
