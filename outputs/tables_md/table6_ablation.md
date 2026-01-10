Table 6 (artifact): Ablation results reconstructed from CSV.

| Setting                       | Acc. repairs   |    TP% |   FN% |   Cand./inst | HC TN/FP   | Reg TN/FP    |   FP% |   Time (s) |
|:------------------------------|:---------------|-------:|------:|-------------:|:-----------|:-------------|------:|-----------:|
| Full system (baseline)        | 2,310          |  99.63 |  0.37 |          6.8 | 1,089/11   | 19,960/40    |  0.21 |        6.4 |
| Omit RCG filtering            | 2,310          |  99.63 |  0.37 |         17.9 | 1,065/35   | 19,821/179   |  1.07 |       12.9 |
| Omit DFA hard masking         | 2,210          |  95.79 |  4.21 |         11.4 | 1,073/27   | 19,911/89    |  0.58 |        9.6 |
| Omit certificate checking     | 2,447          | 100    |  0    |         28.8 | 926/174    | 19,102/898   |  4.2  |        5.2 |
| Omit RCG + $\mathsf{Check}_v$ | 2,447          | 100    |  0    |         37.1 | 817/283    | 18,922/1,078 |  5.34 |        4.6 |
