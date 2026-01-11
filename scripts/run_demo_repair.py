
#!/usr/bin/env python3
from __future__ import annotations
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from safeprompt.pipeline import repair

def main():
    p = argparse.ArgumentParser(description="Run a lightweight SafePrompt-style repair on an example contract.")
    p.add_argument("--contract", default="examples/contracts/ReentrancyVictim.sol", help="Path to Solidity contract")
    p.add_argument("--witness", default="examples/witnesses/reentrancy_withdraw.json", help="Path to witness JSON")
    p.add_argument("--out", default="outputs/demo_repair", help="Output directory")
    args = p.parse_args()

    result = repair(Path(args.contract), Path(args.witness), Path(args.out))
    print("Wrote:", Path(args.out).resolve())
    if result.get("accepted"):
        print("Accepted operator:", result["accepted"]["operator"])
    else:
        print("No repair accepted. See run_summary.json for details.")

if __name__ == "__main__":
    main()
