# Contributing

Contributions must preserve deterministic, secretless execution.

1. Add or update reviewable fixtures.
2. Explain metric and threshold changes.
3. Run `.\scripts\verify.ps1`.
4. Regenerate release artifacts with `python -m cas_evals.release` when fixtures or evaluator behavior changes.
5. Do not include real secrets, customer data, or network-dependent tests.

Changes that alter result shape must update the suite schema, shared-contract validation, release artifacts, and compatibility notes.
