
from __future__ import annotations
import difflib
import re
from dataclasses import dataclass
from typing import Dict, Any, Tuple

@dataclass
class Certificate:
    vuln_class: str
    operator: str
    function: str
    diff_unified: str
    predicates: Dict[str, bool]
    postconditions: Dict[str, bool]
    notes: str

def _abi_compatibility_heuristic(before: str, after: str) -> bool:
    # Check that public/external function signatures are unchanged (rough heuristic).
    sig_re = re.compile(r'\bfunction\s+(\w+)\s*\(([^)]*)\)\s*(public|external)')
    before_sigs = set((m.group(1), re.sub(r'\s+', '', m.group(2))) for m in sig_re.finditer(before))
    after_sigs = set((m.group(1), re.sub(r'\s+', '', m.group(2))) for m in sig_re.finditer(after))
    return before_sigs == after_sigs

def check_patch(before_src: str, after_src: str, vuln_class: str, operator: str, function: str, predicates: Dict[str, bool]) -> Tuple[bool, Certificate]:
    # Postconditions are class-specific. Here we implement a minimal, checkable set.
    post = {}
    notes = []

    post["compiles_placeholder"] = True  # compilation is outside this lightweight artifact
    post["abi_compatible"] = _abi_compatibility_heuristic(before_src, after_src)
    if not post["abi_compatible"]:
        notes.append("ABI compatibility heuristic failed (public/external signatures changed).")

    # Reentrancy postcondition: presence of either a mutex flag or a moved state write before external call (heuristic).
    if vuln_class == "reentrancy":
        has_mutex = "__safeprompt_entered" in after_src
        # heuristic for CEI: look for state write before .call in function text
        fn_re = re.compile(rf'function\s+{re.escape(function)}\b[\s\S]*?\{{([\s\S]*?)\n\s*\}}', re.MULTILINE)
        m = fn_re.search(after_src)
        cei_ok = False
        if m:
            body = m.group(1)
            idx_call = body.find(".call")
            if idx_call != -1:
                # find any assignment before call
                assigns = [m2.start() for m2 in re.finditer(r'=\s*[^=]', body)]
                cei_ok = any(a < idx_call for a in assigns)
        post["reentrancy_guard_present"] = bool(has_mutex or cei_ok)
        if not post["reentrancy_guard_present"]:
            notes.append("Reentrancy postcondition heuristic failed (no guard or effect-before-interaction evidence found).")

    ok = all(post.values())
    diff = "".join(difflib.unified_diff(
        before_src.splitlines(True), after_src.splitlines(True),
        fromfile="before.sol", tofile="after.sol"
    ))

    cert = Certificate(
        vuln_class=vuln_class,
        operator=operator,
        function=function,
        diff_unified=diff,
        predicates=predicates,
        postconditions=post,
        notes="; ".join(notes) if notes else "ok",
    )
    return ok, cert
