---
phase: 02-shared-contracts-and-corpus
plan: "02"
status: complete
completed: 2026-06-11
requirements: [CORP-01]
---

# Plan 02-02 Summary

Added a v0.2 corpus with eight representative golden engineering workflows and six independent adversarial safety risks. Capability labels and tests make corpus coverage explicit and reviewable.

## Verification

- `python -m unittest discover -s tests -v` - 16 tests passed.
- `python -m cas_evals.cli benchmarks/v0.2/golden.json --output artifacts/v0.2-golden.json` - 8/8 passed.
- `python -m cas_evals.cli benchmarks/v0.2/adversarial.json --output artifacts/v0.2-adversarial.json` - 6/6 passed.
- `git diff --check` - passed.

## Deviations from Plan

None - plan executed exactly as written.

## Self-Check: PASSED
