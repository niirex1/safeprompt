
#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
from tabulate import tabulate

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
OUT_MD = REPO_ROOT / "outputs" / "tables_md"
OUT_TEX = REPO_ROOT / "outputs" / "tables_tex"

def _latex_table(df: pd.DataFrame, caption: str, label: str) -> str:
    # three-line table with booktabs
    cols = list(df.columns)
    align = "l" + "c" * (len(cols) - 1)
    header = " & ".join([f"\\textbf{{{c}}}" for c in cols]) + " \\\\"
    rows = []
    for _, r in df.iterrows():
        rows.append(" & ".join(str(r[c]) for c in cols) + " \\\\")
    body = "\n".join(rows)
    return "\n".join([
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        f"\\begin{{tabular}}{{{align}}}",
        "\\toprule",
        header,
        "\\midrule",
        body,
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
        "",
    ])

def _markdown_table(df: pd.DataFrame) -> str:
    return tabulate(df, headers="keys", tablefmt="github", showindex=False)

def main():
    p = argparse.ArgumentParser(description="Reproduce SafePrompt paper tables from CSVs.")
    p.add_argument("--data", default=str(DATA_DIR), help="Directory containing CSV files.")
    p.add_argument("--out_md", default=str(OUT_MD), help="Output directory for markdown tables.")
    p.add_argument("--out_tex", default=str(OUT_TEX), help="Output directory for LaTeX tables.")
    args = p.parse_args()

    data_dir = Path(args.data)
    out_md = Path(args.out_md); out_md.mkdir(parents=True, exist_ok=True)
    out_tex = Path(args.out_tex); out_tex.mkdir(parents=True, exist_ok=True)

    specs = [
        ("table2_reentrancy.csv",
         "Table 2: Reentrancy repair evaluation (SafePrompt).",
         "tab:rq_reentrancy"),
        ("table3_price_manip.csv",
         "Table 3: Price-manipulation repair evaluation (SafePrompt).",
         "tab:rq_price"),
        ("table3_price_manip_fp_breakdown.csv",
         "Table 3 (continued): False-positive breakdown by benign category.",
         "tab:rq_price_fp_breakdown"),
        ("table4_reentrancy_comparison.csv",
         "Table 4: Reentrancy comparison against prior systems.",
         "tab:reentrancy_compare"),
        ("table5_price_manip_comparison_d1.csv",
         "Table 5: Price-manipulation comparison on D1 benchmark.",
         "tab:price_compare_d1"),
        ("table6_ablation.csv",
         "Table 6: Ablation study.",
         "tab:ablation"),
        ("table7_readonly_reentrancy.csv",
         "Table 7: Read-only reentrancy evaluation.",
         "tab:readonly"),
    ]

    for fname, caption, label in specs:
        df = pd.read_csv(data_dir / fname)
        (out_md / f"{Path(fname).stem}.md").write_text(_markdown_table(df) + "\n", encoding="utf-8")
        (out_tex / f"{Path(fname).stem}.tex").write_text(_latex_table(df, caption, label), encoding="utf-8")

    print("Wrote tables to:")
    print(" -", out_md)
    print(" -", out_tex)

if __name__ == "__main__":
    main()
