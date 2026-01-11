# Notes for reviewers

This repository is intended for artifact evaluation and result-layer reproducibility.

- Table regeneration is deterministic and requires no network access.
- The `safeprompt/` module provides a lightweight, runnable reference implementation of the paper’s certified repair loop
  (RCG predicates → operator selection → patch generation → certificate checking). It is not a full release of the
  end-to-end toolchain used for the experiments (which depends on larger corpora and a Solidity build toolchain).
- The demo script `scripts/run_demo_repair.py` shows a concrete patch and a machine-checkable certificate emitted as JSON.
