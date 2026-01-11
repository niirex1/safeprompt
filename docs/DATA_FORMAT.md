# Data format

This artifact stores the final numeric tables reported in the SafePrompt manuscript as CSV files under `data/`.

Conventions:

- `±` uses the paper’s formatting and indicates mean ± standard deviation.
- `Gas_delta_M` and `Gas_cost_M` are reported in **millions of gas (M)**.
- Times are reported in seconds (`*_time_s`) unless the cell explicitly uses `ms`.

Files:

- `table2_reentrancy.csv`: reentrancy repair evaluation (vulnerable + benign splits).
- `table3_price_manip.csv`: price-manipulation repair evaluation (vulnerable + benign splits).
- `table3_price_manip_fp_breakdown.csv`: false-positive breakdown for Table 3.
- `table4_reentrancy_comparison.csv`: system comparison for reentrancy.
- `table5_price_manip_comparison_d1.csv`: D1 baseline comparison for price manipulation.
- `table6_ablation.csv`: ablation settings and outputs.
- `table7_readonly_reentrancy.csv`: read-only reentrancy evaluation.
