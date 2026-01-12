# SafePrompt: Certified Detection and Repair for Solidity Smart Contracts (CCS Artifact)

This repository accompanies the CCS submission **SafePrompt** and is prepared for **double-blind review**.
It provides a deterministic, offline artifact that reproduces the manuscript’s evaluation tables and
demonstrates the paper’s certified repair loop on a small, self-contained example.

The artifact is split into two layers:

1. **Result layer (tables)**: scripts that regenerate all numeric tables reported in the evaluation sections from CSV.
2. **Reference implementation (pipeline)**: a lightweight `safeprompt/` module that runs the paper’s
   detection-to-repair workflow: Repair Context Graph (RCG) predicates → operator-family selection →
   hard-constrained edit proposal → patch candidate generation → certificate checking → accept/abstain.

---

## 📦 Repository contents

| Path | What it contains |
|---|---|
| `safeprompt/` | Reference implementation of the certified repair pipeline (RCG predicates, operator library, certificate checker, and end-to-end pipeline glue). |
| `scripts/reproduce_tables.py` | Regenerates all paper tables from `data/*.csv` into `outputs/tables_md/` and `outputs/tables_tex/`. |
| `scripts/verify_outputs.py` | Verifies that regenerated tables match the expected hashes in `docs/expected_hashes.json`. |
| `scripts/run_demo_repair.py` | Runs a small end-to-end demo repair: reads a Solidity contract + witness JSON, applies SafePrompt-style operators, and writes a patch + certificate to `outputs/demo_repair/`. |
| `data/` | CSV files with the final table numbers reported in the manuscript (evaluation layer only). |
| `figures/` | Paper figures needed for artifact review (e.g., the SafePrompt architecture figure). |
| `docs/DATA_FORMAT.md` | CSV schema notes and units for table regeneration. |
| `docs/expected_hashes.json` | Expected output hashes for deterministic verification. |
| `docs/ARTIFACT_NOTES.md` | Reviewer notes and scope boundaries for the artifact. |

---

## ⚙️ Requirements

| Component | Minimum | Recommended |
|---|---|---|
| OS | Windows 10 / Ubuntu 22.04 / macOS | Ubuntu 22.04 |
| Python | 3.10 | 3.11 |
| RAM | 8 GB | 16 GB |
| Disk | < 1 GB | < 1 GB |

This artifact is **CPU-only**. It does not require GPU.

---

## 🪜 Installation

### Linux/macOS/WSL

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## ▶️ Quick start

### 1) Reproduce manuscript tables (deterministic)

```bash
python scripts/reproduce_tables.py
python scripts/verify_outputs.py
```

If verification succeeds, the regenerated outputs match `docs/expected_hashes.json`.

**Outputs:**
- `outputs/tables_md/` (Markdown tables)
- `outputs/tables_tex/` (LaTeX tables)

### 2) Run the certified repair demo (end-to-end)

```bash
python scripts/run_demo_repair.py
```

This runs a small SafePrompt-style repair on the included example contract and witness.
The demo produces:

- `outputs/demo_repair/patched.sol` (patched contract)
- `outputs/demo_repair/certificate.json` (machine-checkable certificate)
- `outputs/demo_repair/run_summary.json` (pipeline decisions and checks)

You can point the demo at your own inputs:

```bash
python scripts/run_demo_repair.py \
  --contract path/to/Contract.sol \
  --witness  path/to/witness.json \
  --out outputs/my_run
```

---

## 🧾 Mapping to paper components (scripts → claims)

The artifact is designed to let reviewers trace “what code produces what evidence”.

| Paper component | What it checks | Validated by | Key outputs |
|---|---|---|---|
| Evaluation tables (Tables 2–7) | Table regeneration from fixed CSV numbers | `scripts/reproduce_tables.py`, `scripts/verify_outputs.py` | `outputs/tables_md/*.md`, `outputs/tables_tex/*.tex` |
| RCG predicate extraction | Builds RCG-style predicates used for operator applicability filtering | `safeprompt/rcg/build_rcg.py` (used by the pipeline) | Included in `certificate.json` and `run_summary.json` |
| Operator-family selection | Chooses operator families based on vulnerability class and RCG predicates | `safeprompt/operators/library.py` (queried by the pipeline) | `run_summary.json` (“chosen_family”, “candidate_ops”) |
| Hard-constrained edit proposal | Restricts edits to an operator’s admissible action language | Implemented inside `safeprompt/operators/library.py` | Patch metadata in `certificate.json` |
| Certificate checking | Checks postconditions and emits a certificate over the site-local diff | `safeprompt/cert/checker.py` | `certificate.json` (“postconditions”, “diff_unified”) |
| Accept / abstain decision | Accepts only if certificate checks pass; otherwise abstains | `safeprompt/pipeline.py` | `run_summary.json` (“accepted” or “abstained”) |

---

## 📊 Expected outputs (what you should see)

After table reproduction:

```
outputs/
  tables_md/
    table2_reentrancy.md
    table3_price_manip.md
    table3_price_manip_fp_breakdown.md
    table4_reentrancy_compare.md
    table5_price_compare.md
    table6_ablation.md
    table7_readonly_reentrancy.md
  tables_tex/
    table2_reentrancy.tex
    table3_price_manip.tex
    table3_price_manip_fp_breakdown.tex
    table4_reentrancy_compare.tex
    table5_price_compare.tex
    table6_ablation.tex
    table7_readonly_reentrancy.tex
```

After the demo repair:

```
outputs/
  demo_repair/
    patched.sol
    certificate.json
    run_summary.json
```

---

## Notes for reviewers

- The **table layer** is deterministic and offline by construction.
- The `safeprompt/` module is a **runnable reference implementation** of the certified workflow described in the paper.
  It is intentionally lightweight so that it runs without a Solidity toolchain, RPC endpoints, or large trace corpora.
- The full end-to-end experimental pipeline in the manuscript depends on additional corpora and build tooling.
  This artifact focuses on (i) numeric-table reproducibility and (ii) a concrete, executable version of the pipeline logic.

---

## Troubleshooting

| Issue | Fix |
|---|---|
| `ModuleNotFoundError` | Activate the environment and run `pip install -r requirements.txt`. |
| Verification fails | Re-run in a clean environment; ensure Python 3.10–3.11. |
| Windows activation blocked | Use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` or run via CMD. |

---

## Citation

A `CITATION.cff` file is included at the repository root.

---

## License

See `LICENSE` for terms covering the artifact contents.
