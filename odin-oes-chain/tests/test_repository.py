import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class RepositoryFoundationTests(unittest.TestCase):
    def test_required_directories_exist(self):
        for name in ("chain", "contracts", "explorer", "wallet", "infra", "scripts", "docs", "tests", ".github"):
            with self.subTest(name=name):
                self.assertTrue((ROOT / name).is_dir())

    def test_environment_policy_lists_all_environments(self):
        policy = (ROOT / "chain/config/environments.yaml").read_text(encoding="utf-8")
        for environment in ("local", "devnet", "testnet", "mainnet"):
            with self.subTest(environment=environment):
                self.assertIn(f"  {environment}:", policy)

    def test_adr_pins_evm_dependency_pair(self):
        adr = (ROOT / "docs/ADR-001-stack.md").read_text(encoding="utf-8")
        self.assertIn("Cosmos SDK | `v0.54.3`", adr)
        self.assertIn("CometBFT | `v0.39.3`", adr)


if __name__ == "__main__":
    unittest.main()
