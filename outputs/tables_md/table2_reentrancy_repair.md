Table 2 (artifact): Reentrancy repair evaluation reconstructed from CSV.

| Dataset         | Size   | Avg. cand./inst   | Gas Δ (M)   | Repair time (s)   | TP/FN   | TN/FP      |
|:----------------|:-------|:------------------|:------------|:------------------|:--------|:-----------|
| Vulnerable      | 268    | 18.6±7.4          | 0.21±0.34   | 18.4±11.2         | 203/65  | -          |
| High-Complexity | 1,100  | 9.2±4.1           | 0.05±0.12   | 5.8±4.9           | -       | 1,091/9    |
| Regular         | 20,000 | 6.1±3.0           | 0.01±0.06   | 2.3±2.1           | -       | 19,838/162 |
