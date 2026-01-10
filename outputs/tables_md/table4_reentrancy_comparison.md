Table 4 (artifact): Reentrancy comparison reconstructed from CSV.

| System     | Role     | Time             | Flagged   | Confirmed   | Accepted   |    TP% |   FP% |
|:-----------|:---------|:-----------------|:----------|:------------|:-----------|-------:|------:|
| TxSpector  | detector | 217±101 ms       | 49,080    | 2,447       | -          | 100    |  0.06 |
| Sereum     | detector | 1.03 s (99%<4 s) | 3,357     | 2,447       | -          |  99.36 |  0.03 |
| Clue       | detector | 30±1,683 ms      | 2,323     | 2,447       | -          |  99.61 |  0.02 |
| EVMPatch   | repair   | 0.74±0.41 s      | 3,912     | 2,447       | 1,965      |  98.08 |  0.14 |
| Elysium    | repair   | 1.21±0.66 s      | 3,506     | 2,447       | 2,044      |  98.74 |  0.12 |
| AROC       | repair   | 2.87±1.54 s      | 3,104     | 2,447       | 2,018      |  98.93 |  0.1  |
| SafePrompt | repair   | 6.4±3.9 s        | 2,784     | 2,447       | 2,310      |  99.63 |  0.01 |
