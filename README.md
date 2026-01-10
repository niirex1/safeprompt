# SafePrompt CCS Artifact (tables + architecture)

This repository contains the evaluation-layer artifact for the CCS submission **SafePrompt**.
It is prepared for **double-blind review** and is **deterministic** (no network access required).

## What this artifact contains

- The SafePrompt architecture figure used in the paper:
  - `figures/safeprompt_architecture.png`
- CSV files that encode every numeric table reported in the evaluation sections:
  - `data/*.csv`
- Deterministic scripts that regenerate the tables from the CSVs:
  - `scripts/reproduce_tables.py`
  - `scripts/verify_outputs.py`
- Expected-output hashes used for verification:
  - `docs/expected_hashes.json`
- Data-format notes:
  - `docs/DATA_FORMAT.md`

## What this artifact reproduces

Running the scripts reproduces the following paper tables from CSV:

- Table 2: Reentrancy repair evaluation
- Table 3: Price-manipulation repair evaluation (+ false-positive breakdown)
- Table 4: Reentrancy comparison
- Table 5: Price-manipulation comparison (D1 benchmark)
- Table 6: Ablation study
- Table 7: Read-only reentrancy evaluation

Generated files are written to:

- `outputs/tables_md/` (Markdown)
- `outputs/tables_tex/` (LaTeX)

## Quick start (about 1 minute)

### Linux/macOS/WSL
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/reproduce_tables.py
python scripts/verify_outputs.py
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python scripts\reproduce_tables.py
python scripts\verify_outputs.py
```

If verification succeeds, the regenerated outputs match the expected hashes in
`docs/expected_hashes.json`.

## Data files

All table CSVs are in `data/`.

Units follow the manuscript tables:

- `gas_delta_M_*` values are in **millions of gas (M)**, as reported.
- Times are in seconds unless a cell explicitly shows `ms`.

See `docs/DATA_FORMAT.md` for column descriptions and schema.

## Mapping to paper results

Each table CSV corresponds to one paper table. The scripts print the resolved mapping at runtime,
and write both Markdown and LaTeX versions to `outputs/`.

| Paper table | Artifact CSV (default name) | Output files |
|---|---|---|
| Table 2 | `data/table2_reentrancy.csv` | `outputs/tables_*/table2_*` |
| Table 3 | `data/table3_price_manip.csv` | `outputs/tables_*/table3_*` |
| Table 4 | `data/table4_reentrancy_compare.csv` | `outputs/tables_*/table4_*` |
| Table 5 | `data/table5_price_compare.csv` | `outputs/tables_*/table5_*` |
| Table 6 | `data/table6_ablation.csv` | `outputs/tables_*/table6_*` |
| Table 7 | `data/table7_readonly_reentrancy.csv` | `outputs/tables_*/table7_*` |

If your branch uses different filenames, keep the CSVs under `data/` and update the mapping table above
to match the repository.

## Expected outputs

After a successful run you should see:

```
outputs/
  tables_md/
    table2_reentrancy.md
    table3_price_manip.md
    table4_reentrancy_compare.md
    table5_price_compare.md
    table6_ablation.md
    table7_readonly_reentrancy.md

  tables_tex/
    table2_reentrancy.tex
    table3_price_manip.tex
    table4_reentrancy_compare.tex
    table5_price_compare.tex
    table6_ablation.tex
    table7_readonly_reentrancy.tex
```

## Notes for reviewers

- The CSVs reflect the final numeric values reported in the manuscript tables.
- The scripts are deterministic and do not depend on network access.
- The end-to-end synthesis and checking pipeline depends on the contract and trace corpora referenced by
  the paper and the SafePrompt implementation. This artifact focuses on the numeric-result layer used to
  produce the manuscript tables.

## Troubleshooting

| Issue | Fix |
|---|---|
| `ModuleNotFoundError` | Activate the environment and run `pip install -r requirements.txt`. |
| Verification fails | Re-run in a clean environment; avoid editing generated outputs; ensure Python 3.10–3.11. |
| Windows activation blocked | Run PowerShell as Administrator or use CMD activation. |

## Citation

If you use this artifact in academic work, please cite the paper. A `CITATION.cff` file is included
for reference.

## License

See `LICENSE` for terms covering the artifact contents.
