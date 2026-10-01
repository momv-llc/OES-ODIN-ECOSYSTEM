#!/usr/bin/env bash
set -euo pipefail
: "${OES_HOME:?OES_HOME is required}"
: "${OES_NODE_NAME:?OES_NODE_NAME is required}"
: "${OES_P2P_PORT:?OES_P2P_PORT is required}"
while [ ! -f /shared/ready ]; do sleep 1; done
exec oesd start --home "$OES_HOME" --p2p.laddr "tcp://0.0.0.0:${OES_P2P_PORT}" --rpc.laddr tcp://0.0.0.0:26657 --grpc.address 0.0.0.0:9090
