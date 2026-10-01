import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("genesis", ROOT / "scripts/generate_genesis.py")
genesis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(genesis)


class TokenomicsTests(unittest.TestCase):
    def policy(self):
        return json.loads((ROOT / "tokenomics.yaml").read_text())

    def test_supply_and_allocations(self):
        allocations = genesis.validate(self.policy())
        self.assertEqual(sum(item["amount"] for item in allocations), 10**27)
        self.assertEqual(allocations[0]["amount"], 300_000_000 * 10**18)

    def test_native_decimals(self):
        policy = self.policy()
        self.assertEqual((policy["base_denom"], policy["display_denom"], policy["decimals"]), ("uoes", "OES", 18))

    def test_invalid_allocation_fails(self):
        policy = self.policy()
        policy["allocations"][0]["percent"] = 29
        with self.assertRaises(ValueError):
            genesis.validate(policy)

    def test_overflow_fails(self):
        policy = self.policy()
        policy["genesis_supply_oes"] = str(2**256)
        with self.assertRaises(ValueError):
            genesis.validate(policy)


if __name__ == "__main__":
    unittest.main()
