
from __future__ import annotations
import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

from .utils import Witness
from .rcg.build_rcg import build_rcg
from .operators.library import operator_families
from .cert.checker import check_patch

def repair(solidity_path: Path, witness_path: Path, out_dir: Path) -> Dict[str, Any]:
    """Run a lightweight SafePrompt-style detection-to-repair pass.

    Inputs are intentionally simple for artifact reproducibility:
    - solidity_path: path to the contract
    - witness_path: JSON with vuln_class + function (+ optional hints)
    Outputs:
    - patched contract, certificate JSON, unified diff
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    src = solidity_path.read_text(encoding="utf-8")
    wit = Witness.from_json(json.loads(witness_path.read_text(encoding="utf-8")))

    rcg = build_rcg(src, wit.function)
    fams = operator_families()
    ops = fams.get(wit.vuln_class, [])
    applicable_ops = [op for op in ops if op.applicable(rcg.predicates)]

    results = {
        "contract": solidity_path.name,
        "function": wit.function,
        "vuln_class": wit.vuln_class,
        "predicates": rcg.predicates,
        "attempted": [],
        "accepted": None,
    }

    for op in applicable_ops:
        patched, meta = op.apply(src, wit.function)
        ok, cert = check_patch(src, patched, wit.vuln_class, op.name, wit.function, rcg.predicates)
        attempt = {
            "operator": op.name,
            "family": op.family,
            "meta": meta,
            "accepted": bool(ok),
            "certificate": asdict(cert),
        }
        results["attempted"].append(attempt)
        if ok:
            # write artifacts
            (out_dir / "patched.sol").write_text(patched, encoding="utf-8")
            (out_dir / "certificate.json").write_text(json.dumps(asdict(cert), indent=2), encoding="utf-8")
            (out_dir / "diff.patch").write_text(cert.diff_unified, encoding="utf-8")
            results["accepted"] = {"operator": op.name, "meta": meta}
            break

    (out_dir / "run_summary.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results
