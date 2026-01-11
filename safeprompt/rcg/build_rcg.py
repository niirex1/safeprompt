
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

EXTERNAL_CALL_RE = re.compile(r'\.(call|delegatecall|staticcall)\b|\btransfer\(|\bsend\(')

@dataclass
class RCGNode:
    kind: str
    line: int
    text: str

@dataclass
class RepairContextGraph:
    contract_name: str
    function: str
    nodes: List[RCGNode]
    edges: List[Tuple[int, int]]
    predicates: Dict[str, bool]

def _find_contract_name(src: str) -> str:
    m = re.search(r'\bcontract\s+(\w+)\b', src)
    return m.group(1) if m else "UnknownContract"

def _extract_function_block(src_lines: List[str], fn_name: str) -> Tuple[int, int]:
    # naive brace matching starting at function signature line
    start = None
    for i, line in enumerate(src_lines, start=1):
        if re.search(rf'\bfunction\s+{re.escape(fn_name)}\b', line):
            start = i
            break
    if start is None:
        raise ValueError(f"function '{fn_name}' not found")
    brace = 0
    began = False
    for j in range(start, len(src_lines) + 1):
        line = src_lines[j-1]
        for ch in line:
            if ch == '{':
                brace += 1
                began = True
            elif ch == '}':
                brace -= 1
        if began and brace == 0:
            return start, j
    return start, len(src_lines)

def build_rcg(solidity_source: str, fn_name: str) -> RepairContextGraph:
    """Build a lightweight Repair Context Graph (RCG).

    This implementation is deliberately conservative and deterministic:
    it captures (a) external call sites and (b) state writes in the same function.
    Predicates are simple boolean flags used for operator applicability.
    """
    lines = solidity_source.splitlines()
    contract = _find_contract_name(solidity_source)
    start, end = _extract_function_block(lines, fn_name)

    nodes: List[RCGNode] = []
    edges: List[Tuple[int,int]] = []
    last_node_idx = None

    has_external_call = False
    has_state_write = False
    has_require_guard = False

    for ln in range(start, end + 1):
        text = lines[ln-1]
        stripped = text.strip()

        if "require(" in stripped or "assert(" in stripped:
            has_require_guard = True

        if EXTERNAL_CALL_RE.search(stripped):
            has_external_call = True
            nodes.append(RCGNode(kind="external_call", line=ln, text=stripped))
            if last_node_idx is not None:
                edges.append((last_node_idx, len(nodes)-1))
            last_node_idx = len(nodes)-1
            continue

        # heuristic state write: assignment to mapping or storage var
        if re.search(r'\b\w+\s*(\[.*?\])?\s*\+=|\b\w+\s*(\[.*?\])?\s*-=', stripped) or re.search(r'=\s*[^=]', stripped):
            # filter out local declarations to reduce noise
            if "memory" not in stripped and "calldata" not in stripped and not stripped.startswith("//") and "==" not in stripped:
                has_state_write = True
                nodes.append(RCGNode(kind="state_write", line=ln, text=stripped))
                if last_node_idx is not None:
                    edges.append((last_node_idx, len(nodes)-1))
                last_node_idx = len(nodes)-1

    predicates = {
        "has_external_call": has_external_call,
        "has_state_write": has_state_write,
        "has_require_guard": has_require_guard,
    }
    return RepairContextGraph(
        contract_name=contract,
        function=fn_name,
        nodes=nodes,
        edges=edges,
        predicates=predicates,
    )
