#!/usr/bin/env python3
"""Validate the repository baseline without requiring application dependencies."""
from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED = ("chain", "contracts", "explorer", "wallet", "infra", "scripts", "docs", "tests", ".github")
FORBIDDEN = ("TO" + "DO", "FIX" + "ME", "CHANGE" + "_ME", "YOUR" + "_RPC", "example" + ".com")
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".py", ".go", ".ts", ".tsx", ".sol", ".toml", ".json", ".txt"}


def relevant_files() -> list[pathlib.Path]:
    return [path for path in ROOT.rglob("*") if path.is_file() and path.suffix in TEXT_SUFFIXES and ".git" not in path.parts]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    for directory in REQUIRED:
        if not (ROOT / directory).is_dir():
            errors.append(f"missing required directory: {directory}")
    for path in relevant_files():
        content = path.read_text(encoding="utf-8")
        for marker in FORBIDDEN:
            if marker in content:
                errors.append(f"forbidden marker {marker!r} in {path.relative_to(ROOT)}")
        if args.format and content and not content.endswith("\n"):
            errors.append(f"missing trailing newline: {path.relative_to(ROOT)}")
    if errors:
        print("repository validation failed:", *errors, sep="\n- ", file=sys.stderr)
        return 1
    print("repository foundation validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
