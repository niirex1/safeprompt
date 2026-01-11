
from __future__ import annotations
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Tuple

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

@dataclass(frozen=True)
class Witness:
    vuln_class: str
    function: str
    external_call_line: int | None = None
    state_write_line: int | None = None
    extra: Dict[str, Any] | None = None

    @staticmethod
    def from_json(obj: Dict[str, Any]) -> "Witness":
        return Witness(
            vuln_class=str(obj.get("vuln_class", "unknown")),
            function=str(obj.get("function", "")),
            external_call_line=obj.get("external_call_line"),
            state_write_line=obj.get("state_write_line"),
            extra={k: v for k, v in obj.items() if k not in {"vuln_class","function","external_call_line","state_write_line"}},
        )
