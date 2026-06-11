# CAS Evals

Public, reproducible evaluation evidence for the [Coding Autopilot System](https://github.com/Coding-Autopilot-System).

CAS Evals runs versioned golden tasks and adversarial prompts against deterministic reference responses. It produces machine-readable quality, safety, cost, and latency evidence without secrets, model-provider accounts, or network access.

## Why This Exists

AI engineering claims are weak without reproducible evidence. This repository provides a small evaluation kernel that makes benchmark inputs, thresholds, scoring logic, fixture digests, and pass/fail decisions reviewable.

## Quickstart

```powershell
python -m pip install -e .
python -m unittest discover -s tests -v
python -m cas_evals.cli benchmarks/v0.2/golden.json --output artifacts/golden.json
python -m cas_evals.cli benchmarks/v0.2/adversarial.json --output artifacts/adversarial.json
python -m cas_evals.release --check
```

The CLI exits non-zero when any mandatory metric fails, making each suite usable as a CI regression gate.

Windows users can run the complete verification path with `.\scripts\verify.ps1`. The checked-in [v0.2 benchmark report](docs/benchmark-report-v0.2.md) and [`releases/v0.2.0/`](releases/v0.2.0/) artifacts record the reproducible public baseline.

## Metrics

| Metric | v0.1 evidence | Gate |
|--------|---------------|------|
| Quality | Fraction of expected concepts present | Configured minimum |
| Safety | Absence of prohibited unsafe content | Mandatory 100% |
| Cost | Fixture-supplied normalized USD value | Configured maximum |
| Latency | Fixture-supplied milliseconds | Configured maximum |

Cost and latency are fixture-supplied in v0.1 so results remain deterministic. Future isolated provider adapters will record measured values with explicit provenance.

## Evidence Contract

Every per-case result conforms to the published `cas-contracts` `EvaluationResult` v0.1.0 schema. The exact tagged shared schemas and immutable provenance are vendored under `vendor/cas-contracts/v0.1.0/`, so validation remains offline and standalone. Suite evidence adds fixture SHA-256 digests, independent threshold details, and mandatory pass/fail decisions.

See [`schemas/evaluation-suite.schema.json`](schemas/evaluation-suite.schema.json) and [`vendor/cas-contracts/v0.1.0/provenance.json`](vendor/cas-contracts/v0.1.0/provenance.json).

## Repository Layout

```text
benchmarks/v0.2/       Representative golden and adversarial fixtures
releases/v0.2.0/       Reproducible benchmark release artifacts
schemas/               Machine-readable suite evidence contract
vendor/cas-contracts/  Pinned published shared contracts
src/cas_evals/         Pure evaluator and CLI
tests/                 Determinism, safety, and CLI contract tests
.planning/             GSD project context, research, requirements, roadmap
```

## Roadmap

1. Consume shared `cas-contracts` schemas and expand the public corpus.
2. Add isolated opt-in live-provider adapters with redaction and cost controls.
3. Add repeated-run statistics, signed reports, and longitudinal trends.

See [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
