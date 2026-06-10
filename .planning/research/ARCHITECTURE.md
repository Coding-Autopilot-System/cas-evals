# Architecture Research

## Components

1. Fixture loader validates benchmark input shape at the boundary.
2. Deterministic evaluator computes independent metric evidence.
3. Result model emits a stable contract-aligned JSON document.
4. CLI runs suites, writes evidence, and returns a gating exit code.
5. Tests verify scoring, determinism, schema shape, and CLI behavior.

## Data Flow

`fixture JSON -> loader -> evaluator -> metric evidence -> result JSON -> CI gate`

## Build Order

Define contracts and fixtures first, implement pure scoring second, add CLI and evidence output third, then enforce behavior in tests and CI.
