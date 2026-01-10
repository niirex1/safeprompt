#!/usr/bin/env python3
"""Verify artifact outputs match the shipped expected hashes.

Usage:
  python scripts/reproduce_tables.py
  python scripts/verify_outputs.py
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ROOT / "docs" / "expected_hashes.json"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    if not EXPECTED.exists():
        print(f"Missing expected hashes: {EXPECTED}")
        return 2

    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    bad = []
    for rel, want in expected.items():
        p = ROOT / rel
        if not p.exists():
            bad.append((rel, "missing", want))
            continue
        got = sha256_file(p)
        if got != want:
            bad.append((rel, got, want))

    if bad:
        print("Verification FAILED:")
        for rel, got, want in bad:
            print(f"  {rel}\n    got : {got}\n    want: {want}")
        return 1

    print("Verification OK: outputs match expected hashes.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
