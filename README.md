# SafePrompt

SafePrompt is a template-constrained repair pipeline for Solidity vulnerabilities. It couples detection with patch synthesis and validation: a localized context graph is extracted, applicable verified repair templates are retrieved, candidates are decoded under template-induced constraints, and a repair is accepted only if it passes compilation, ABI and storage compatibility checks, project tests, and template-derived SMT obligations.

This repository is the companion artifact for the SafePrompt manuscript.

## Pipeline (as in the paper)

1. **Context extraction**: build the Repair Context Graph (RCG) for a localized vulnerable site using external-call attributes, control reachability, and storage read/write dependencies.
2. **Template mining and retrieval**: rank and select applicable templates for the site using predicates over the RCG.
3. **Template-constrained decoding**: compile the chosen template instance into a DFA and apply hard masking during decoding.
4. **Layered validation**: accept a patch only if it passes all gates:
   - compilation
   - ABI and storage stability
   - project tests
   - template-induced SMT postconditions (bounded semantics, configurable loop-unroll depth, solver timeout default 10s)

Accepted repairs emit a unified diff, discharged SMT obligations, and counterexamples when SMT fails.

## Evaluation (summary)

The evaluation is organized around four research questions:

- **RQ1**: functional correctness and safety compliance under the four acceptance gates.
- **RQ2**: efficiency (end-to-end time, candidate count, validation overhead) under fixed budgets.
- **RQ3**: comparison against state-of-the-art dynamic analysis tools and repair baselines.
- **RQ4**: ablations of key components:
  - RCG-based applicability filtering and retrieval
  - template-to-DFA hard masking during decoding
  - layered validation with SMT postconditions

Datasets used in the paper:
- **Vulnerable**: all vulnerable functions in the held-out repair set (N = 780). The repair set includes 268 reentrancy and 214 authorization vulnerabilities; the remaining instances cover arithmetic and logic faults.
- **Non-vulnerable High-Complexity**: top 1,100 non-vulnerable functions by estimated gas and control-flow size (from the same projects, with vulnerable functions removed).
- **Non-vulnerable Regular**: 20,000 randomly sampled non-vulnerable functions (from the same projects, with vulnerable functions removed).

## Repository layout

- `safeprompt/` Core pipeline and CLI.
- `graph/` RCG schema, Gremlin server config, and graph queries for context extraction.
- `templates/` Template specs, actions, and compilation to DFA constraints.
- `decode/` Constrained decoding (DFA masking, beam utilities).
- `validate/` Acceptance gates (compile, ABI/storage, tests, SMT) and artifact emission.
- `baselines/` Baseline runners and adapters (includes a Clue adapter placeholder).
- `configs/` Default pipeline and evaluation configs.
- `docs/` Reproducibility notes, dataset notes, template and SMT specs.

## Quickstart (local)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
