
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

@dataclass(frozen=True)
class Operator:
    name: str
    family: str
    description: str
    applicable: Callable[[Dict[str, bool]], bool]
    apply: Callable[[str, str], Tuple[str, Dict[str, str]]]
    # apply(sol_src, fn_name) -> (new_src, metadata)

def op_mutex_guard() -> Operator:
    def applicable(pred: Dict[str, bool]) -> bool:
        return pred.get("has_external_call", False)

    def apply(src: str, fn_name: str):
        # Insert a simple nonReentrant guard pattern.
        # This is a minimal patch that avoids new imports.
        guard_decl = "    bool private __safeprompt_entered;\n"
        require_line = "        require(!__safeprompt_entered, \"REENTRANCY\");\n        __safeprompt_entered = true;\n"
        release_line = "        __safeprompt_entered = false;\n"

        lines = src.splitlines(True)
        # add guard state var after contract opening brace
        out = []
        inserted_decl = False
        for i, line in enumerate(lines):
            out.append(line)
            if (not inserted_decl) and line.strip().startswith("contract") and "{" in line:
                out.append(guard_decl)
                inserted_decl = True

        src2 = "".join(out)

        # insert require at function start and release before function return/end
        lines = src2.splitlines(True)
        out = []
        in_fn = False
        brace = 0
        inserted_req = False
        for line in lines:
            if (not in_fn) and ("function "+fn_name) in line:
                in_fn = True
            if in_fn:
                if "{" in line:
                    brace += line.count("{")
                    if (not inserted_req) and brace > 0:
                        out.append(line)
                        out.append(require_line)
                        inserted_req = True
                        continue
                brace -= line.count("}")
                if "}" in line and brace == 0:
                    # before closing brace
                    out.append(release_line)
                    out.append(line)
                    in_fn = False
                    continue
            out.append(line)

        return ("".join(out), {"guard": "bool __safeprompt_entered", "pattern": "mutex_guard"})

    return Operator(
        name="mutex_guard",
        family="reentrancy",
        description="Insert a simple mutex-style nonReentrant guard within the target function.",
        applicable=applicable,
        apply=apply,
    )

def op_cei_reorder() -> Operator:
    def applicable(pred: Dict[str, bool]) -> bool:
        # CEI reorder is meaningful only if both a state write and an external call exist.
        return pred.get("has_external_call", False) and pred.get("has_state_write", False)

    def apply(src: str, fn_name: str):
        # Heuristic: move the first state write line before the first external call line within the function.
        lines = src.splitlines(True)
        out = []
        in_fn = False
        brace = 0
        fn_lines = []
        prefix = []
        suffix = []
        for line in lines:
            if (not in_fn) and ("function "+fn_name) in line:
                in_fn = True
            if not in_fn:
                prefix.append(line)
                continue
            fn_lines.append(line)
            if "{" in line:
                brace += line.count("{")
            brace -= line.count("}")
            if in_fn and brace == 0 and "}" in line:
                in_fn = False
                suffix = lines[len(prefix)+len(fn_lines):]
                break

        block = "".join(fn_lines)
        blk_lines = block.splitlines(True)

        ext_idx = None
        st_idx = None
        for i, l in enumerate(blk_lines):
            if ext_idx is None and (".call" in l or ".transfer(" in l or ".send(" in l):
                ext_idx = i
            if st_idx is None and ("=" in l and "==" not in l and "require(" not in l and "assert(" not in l):
                st_idx = i
        if ext_idx is None or st_idx is None or st_idx < ext_idx:
            return (src, {"pattern": "cei_reorder", "note": "no-op"})
        # move st line before ext line
        st_line = blk_lines.pop(st_idx)
        blk_lines.insert(ext_idx, st_line)
        new_block = "".join(blk_lines)
        return ("".join(prefix) + new_block + "".join(suffix), {"pattern": "cei_reorder", "moved_line": st_line.strip()})

    return Operator(
        name="cei_reorder",
        family="reentrancy",
        description="Reorder within the function to enforce checks-effects-interactions, moving a state update before the first external call when safe.",
        applicable=applicable,
        apply=apply,
    )

def operator_families() -> Dict[str, List[Operator]]:
    return {
        "reentrancy": [op_cei_reorder(), op_mutex_guard()],
    }
