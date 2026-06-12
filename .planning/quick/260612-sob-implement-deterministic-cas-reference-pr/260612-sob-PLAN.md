---
status: complete
task: deterministic cas-reference-product golden path
---

# Quick Task 260612-sob Plan

## Goal

Add an opt-in, executable `cas-reference-product` HTTP evaluation path without weakening the existing offline evaluator.

## Must Haves

- Score the actual `POST /api/v1/workflows` returned `output`.
- Preserve and verify `correlationId`, `promptId`, `runId`, and trace context in deterministic evidence.
- Support golden and adversarial fixture suites.
- Keep persisted timing normalized and byte-stable.
- Keep the existing offline CLI and release path unchanged.
- Add focused tests, reference-product corpus fixtures, documentation, and CI validation.

## Tasks

1. Add a standard-library reference-product adapter and CLI opt-in.
2. Add deterministic reference-product golden/adversarial corpora and regression tests.
3. Update documentation, CI, GSD state, and run all verification gates.

## Verification

- `python -m unittest discover -s tests -v`
- `python -m cas_evals.cli benchmarks/v0.2/golden.json`
- `python -m cas_evals.cli benchmarks/v0.2/adversarial.json`
- `python -m cas_evals.release --check`
- `git diff --check`
