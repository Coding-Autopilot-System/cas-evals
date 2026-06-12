---
status: complete
completed: 2026-06-12
---

# Quick Task 260612-sob Summary

Implemented an opt-in deterministic HTTP adapter for the local
`cas-reference-product` workflow endpoint while preserving the existing offline
evaluation and release paths.

## Delivered

- Actual returned workflow output is scored for quality and safety.
- Lifecycle metadata and trace context are generated deterministically, verified
  against returned events, and preserved in evaluation evidence.
- Persisted live evidence excludes server timestamps and endpoint addresses and
  uses normalized fixture timing.
- Golden and adversarial reference-product corpora pass against the actual local
  sibling service.
- HTTP, CLI, metadata-drift, actual-output, determinism, and failure-path tests
  run in CI.
- User documentation describes the local executable golden path.

## Commits

- `2a89a9a` - deterministic reference-product evaluation and tests
- `aaeed60` - integration documentation and CI coverage
