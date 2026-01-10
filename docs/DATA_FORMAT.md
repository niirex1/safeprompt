# Data format

## table2_reentrancy_repair.csv
Columns:
- dataset: {Vulnerable, High-Complexity, Regular}
- size: number of functions
- avg_candidates_mean/std: mean and std. dev. of candidate patches evaluated per instance
- gas_delta_M_mean/std: mean and std. dev. of gas delta, in millions of gas (M)
- repair_time_s_mean/std: mean and std. dev. of end-to-end repair time (seconds)
- tp/fn/tn/fp: counts where applicable
- tp_percent/fn_percent/tn_percent/fp_percent: percentages where applicable

## table3_price_manip_repair.csv
Same schema as Table 2, for the price-manipulation class.

## table3_fp_breakdown.csv
False-positive category breakdown from Table 3:
- dataset: {High-Complexity, Regular}
- category: category label used in the paper
- fp_count: number of false positives in that category
- fp_total: total false positives for the dataset

## table4_reentrancy_comparison.csv
- analysis_or_repair_time: as reported in the paper (string, preserves units)
- flagged_tp_fp: number of functions flagged as TP+FP by the system
- confirmed_reentrancy: number of confirmed reentrancy cases in the benchmark
- accepted_repairs: number of accepted repairs (repair systems only)
- tp_percent/fn_percent/tn_percent/fp_percent: percentages as reported

## table5_price_manip_comparison.csv
- detected: number of detected attacks on the D1 benchmark
- repaired: number of repaired (accepted) cases, if applicable
- repair_percent: repaired / 54 * 100 for systems that perform repair

## table6_ablation.csv
- cand_per_instance: average candidates per vulnerable instance evaluated
- high_complexity_tn/fp and regular_tn/fp: outcomes on non-vulnerable sets
- fp_percent: FP rate on the non-vulnerable sets, as reported
- mean_time_s: mean end-to-end time per instance (seconds), as reported

## table7_readonly_reentrancy.csv
Same schema as Table 2, for the read-only reentrancy setting.
