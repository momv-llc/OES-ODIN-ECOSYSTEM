#!/usr/bin/env python3
"""Generate and validate a native-uoes genesis from tokenomics policy."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_policy(path: pathlib.Path) -> dict:
    # JSON is valid YAML 1.2 and keeps generation dependency-free.
    return json.loads(path.read_text(encoding="utf-8"))


def validate(policy: dict) -> list[dict]:
    required = {"chain_id", "evm_chain_id", "base_denom", "display_denom", "decimals", "genesis_supply_oes", "allocations"}
    missing = required - policy.keys()
    if missing:
        raise ValueError(f"missing tokenomics fields: {', '.join(sorted(missing))}")
    if policy["base_denom"] != "uoes" or policy["display_denom"] != "OES" or policy["decimals"] != 18:
        raise ValueError("native denomination policy must be uoes / OES with 18 decimals")
    supply = int(policy["genesis_supply_oes"])
    if supply <= 0 or supply > (2**256 - 1) // 10**18:
        raise ValueError("genesis supply is outside supported integer range")
    allocations = policy["allocations"]
    if not allocations or sum(item["percent"] for item in allocations) != 100:
        raise ValueError("allocation percentages must sum to 100")
    seen = set()
    result = []
    for item in allocations:
        name, percent = item["name"], item["percent"]
        if name in seen or not isinstance(percent, int) or percent <= 0:
            raise ValueError("allocation names must be unique and percentages positive integers")
        seen.add(name)
        amount = supply * 10**18 * percent // 100
        if amount > 2**256 - 1:
            raise ValueError("allocation overflows uint256")
        result.append({"name": name, "amount": amount, "percent": percent})
    if sum(item["amount"] for item in result) != supply * 10**18:
        raise ValueError("sum of allocations does not equal genesis supply")
    return result


def run(command: list[str], input_text: str | None = None) -> str:
    completed = subprocess.run(command, input=input_text, text=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return completed.stdout


def bech32_address(name: str) -> str:
    charset = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
    payload = hashlib.sha256(f"oes-genesis:{name}".encode()).digest()[:20]
    values = [0] + convert_bits(payload, 8, 5, True)
    expanded = [ord(char) >> 5 for char in "oes"] + [0] + [ord(char) & 31 for char in "oes"]
    checksum = polymod(expanded + values + [0] * 6) ^ 1
    return "oes1" + "".join(charset[value] for value in values + [(checksum >> 5 * (5 - index)) & 31 for index in range(6)])


def polymod(values: list[int]) -> int:
    generator = (0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3)
    check = 1
    for value in values:
        top = check >> 25
        check = (check & 0x1FFFFFF) << 5 ^ value
        for index in range(5):
            if (top >> index) & 1:
                check ^= generator[index]
    return check


def convert_bits(data: bytes, from_bits: int, to_bits: int, pad: bool) -> list[int]:
    accumulator, bits, result = 0, 0, []
    for value in data:
        accumulator = (accumulator << from_bits) | value
        bits += from_bits
        while bits >= to_bits:
            bits -= to_bits
            result.append((accumulator >> bits) & ((1 << to_bits) - 1))
    if pad and bits:
        result.append((accumulator << (to_bits - bits)) & ((1 << to_bits) - 1))
    return result


def generate(binary: pathlib.Path, policy: dict, allocations: list[dict], output: pathlib.Path) -> None:
    with tempfile.TemporaryDirectory(prefix="oes-genesis-") as temporary:
        home = pathlib.Path(temporary)
        run([str(binary), "init", "genesis", "--chain-id", policy["chain_id"], "--home", str(home)])
        genesis_path = home / "config" / "genesis.json"
        genesis = json.loads(genesis_path.read_text(encoding="utf-8"))
        genesis["genesis_time"] = "2026-01-01T00:00:00Z"
        accounts, balances = [], []
        for number, item in enumerate(allocations):
            address = bech32_address(item["name"])
            item["address"] = address
            accounts.append({"@type": "/cosmos.auth.v1beta1.BaseAccount", "address": address, "pub_key": None, "account_number": str(number), "sequence": "0"})
            balances.append({"address": address, "coins": [{"denom": policy["base_denom"], "amount": str(item["amount"])}]})
        genesis["app_state"]["auth"]["accounts"] = accounts
        genesis["app_state"]["bank"]["balances"] = balances
        genesis["app_state"]["bank"]["supply"] = [{"denom": policy["base_denom"], "amount": str(sum(item["amount"] for item in allocations))}]
        genesis["app_state"]["bank"]["denom_metadata"] = [{
            "description": "Native asset of OES Chain",
            "denom_units": [{"denom": "uoes", "exponent": 0}, {"denom": "OES", "exponent": 18}],
            "base": "uoes", "display": "OES", "name": "OES", "symbol": "OES",
        }]
        genesis["app_state"]["evm"]["params"]["evm_denom"] = policy["base_denom"]
        genesis["app_state"]["mint"]["params"]["mint_denom"] = policy["base_denom"]
        encoded = json.dumps(genesis, sort_keys=True, separators=(",", ":")) + "\n"
        output.write_text(encoded, encoding="utf-8")
        genesis_path.write_text(encoded, encoding="utf-8")
        run([str(binary), "validate-genesis", "--home", str(home)])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=pathlib.Path, default=ROOT / "tokenomics.yaml")
    parser.add_argument("--binary", type=pathlib.Path, default=ROOT / "bin" / "oesd")
    parser.add_argument("--output", type=pathlib.Path, default=ROOT / "genesis.json")
    parser.add_argument("--validate-only", action="store_true")
    arguments = parser.parse_args()
    try:
        policy = load_policy(arguments.policy)
        allocations = validate(policy)
        if arguments.validate_only:
            print(json.dumps(allocations, sort_keys=True))
            return 0
        generate(arguments.binary, policy, allocations, arguments.output)
        print(f"wrote {arguments.output}")
        return 0
    except (ValueError, subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"genesis generation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
