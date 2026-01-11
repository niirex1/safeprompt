#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from safeprompt.utils import sha256_file  # noqa: E402

def main():
    p = argparse.ArgumentParser(description="Verify reproduced table outputs against expected hashes.")
    p.add_argument("--expected", default=str(REPO_ROOT / "docs" / "expected_hashes.json"))
    p.add_argument("--outputs", default=str(REPO_ROOT / "outputs"))
    args = p.parse_args()

    expected_path = Path(args.expected)

    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    ok = True
    for rel, h in expected.items():
        path = REPO_ROOT / rel
        if not path.exists():
            print("MISSING:", rel)
            ok = False
            continue
        got = sha256_file(path)
        if got != h:
            print("MISMATCH:", rel)
            print(" expected:", h)
            print(" got     :", got)
            ok = False

    if ok:
        print("OK: all outputs match expected hashes.")
        return 0
    print("Verification failed.")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
