# SafePrompt CCS Artifact (tables + architecture)

This package is meant for double-blind review. It contains:
- The SafePrompt architecture figure used in the paper (`figures/safeprompt_architecture.png`).
- CSV files that encode every numeric table reported in the manuscript sections on evaluation.
- Deterministic scripts that regenerate the tables from the CSVs.

## What this artifact reproduces

Running the scripts reproduces the following paper tables from CSV:
- Table 2: Reentrancy repair evaluation
- Table 3: Price-manipulation repair evaluation (+ false-positive breakdown)
- Table 4: Reentrancy comparison
- Table 5: Price-manipulation comparison (D1 benchmark)
- Table 6: Ablation study
- Table 7: Read-only reentrancy evaluation

The generated files are written to:
- `outputs/tables_md/` (markdown)
- `outputs/tables_tex/` (LaTeX)

## Quick start (about 1 minute)

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/reproduce_tables.py
python scripts/verify_outputs.py
```

If verification succeeds, the regenerated outputs match the expected hashes shipped in `docs/expected_hashes.json`.

## Data files

All table CSVs are in `data/`. Units:
- `gas_delta_M_*` values are in **millions of gas** (M), as reported in the manuscript tables.
- Times are in seconds unless a cell explicitly shows ms.

See `docs/DATA_FORMAT.md` for column descriptions.

## Notes for reviewers

- The CSVs are derived from the final numbers reported in the manuscript.
- The scripts are deterministic and do not depend on network access.
- The full end-to-end patch synthesis and SMT checking pipeline depends on the released victim-contract and trace corpora referenced by the paper, plus the SafePrompt implementation itself. This artifact focuses on the numeric-result layer used to produce the manuscript tables.
