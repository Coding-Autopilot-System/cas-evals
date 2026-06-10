# Stack Research

## Recommendation

- Python 3.11+ standard library for the deterministic evaluator and CLI.
- JSON Schema Draft 2020-12 document for interoperable result validation.
- `unittest` for zero-dependency verification.
- GitHub Actions for Linux and Windows reproducibility checks.

## Rationale

An evaluation framework is trusted when its scoring logic is inspectable, its inputs are versioned, and its outputs can be independently validated. Avoiding runtime dependencies in v0.1 reduces supply-chain and installation variability.
