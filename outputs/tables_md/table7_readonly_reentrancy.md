| Split                         | Example       |   Size | Gas_cost_M   | Analysis_or_repair_time_s   | TP   | FN   | TN    | FP   |
|-------------------------------|---------------|--------|--------------|-----------------------------|------|------|-------|------|
| Attack (read-only reentrancy) | sentiment.xyz |      1 | 5.94±1.76    | 2.13±1.38                   | 1    | 0    | -     | -    |
| Attack (read-only reentrancy) | dForce        |      1 | 5.94±1.76    | 2.13±1.38                   | 1    | 0    | -     | -    |
| High-gas benign               | -             |   1077 | 0.24±0.29    | 0.09±0.05                   | -    | -    | 1074  | 3    |
| Regular benign                | -             |  19985 | 0.24±0.29    | 0.09±0.05                   | -    | -    | 19941 | 44   |
