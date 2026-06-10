# CAS Evals

Public, reproducible evaluation evidence for the [Coding Autopilot System](https://github.com/Coding-Autopilot-System).

CAS Evals runs versioned golden tasks and adversarial prompts against deterministic reference responses. It produces machine-readable quality, safety, cost, and latency evidence without secrets, model-provider accounts, or network access.

## Why This Exists

AI engineering claims are weak without reproducible evidence. This repository provides a small evaluation kernel that makes benchmark inputs, thresholds, scoring logic, fixture digests, and pass/fail decisions reviewable.

## Quickstart

```powershell
python -m pip install -e .
python -m unittest discover -s tests -v
python -m cas_evals.cli benchmarks/v0.1/golden.json --output artifacts/golden.json
python -m cas_evals.cli benchmarks/v0.1/adversarial.json --output artifacts/adversarial.json
```

The CLI exits non-zero when any mandatory metric fails, making each suite usable as a CI regression gate.

Windows users can run the complete verification path with `.\scripts\verify.ps1`. The checked-in [v0.1 benchmark report](docs/benchmark-report-v0.1.md) records the initial public baseline.

## Metrics

| Metric | v0.1 evidence | Gate |
|--------|---------------|------|
| Quality | Fraction of expected concepts present | Configured minimum |
| Safety | Absence of prohibited unsafe content | Mandatory 100% |
| Cost | Fixture-supplied normalized USD value | Configured maximum |
| Latency | Fixture-supplied milliseconds | Configured maximum |

Cost and latency are fixture-supplied in v0.1 so results remain deterministic. Future isolated provider adapters will record measured values with explicit provenance.

## Evidence Contract

Results include `schemaVersion`, `evaluatorVersion`, `caseId`, `correlationId`, fixture SHA-256 digest, independent metric details, and pass/fail status. The schema is conceptually aligned with the CAS lifecycle and will consume versioned `cas-contracts` artifacts in the next phase.

See [`schemas/evaluation-result.schema.json`](schemas/evaluation-result.schema.json).

## Repository Layout

```text
benchmarks/v0.1/       Golden and adversarial fixtures
schemas/               Machine-readable result contract
src/cas_evals/         Pure evaluator and CLI
tests/                 Determinism, safety, and CLI contract tests
.planning/             GSD project context, research, requirements, roadmap
```

## Roadmap

1. Consume shared `cas-contracts` schemas and expand the public corpus.
2. Add isolated opt-in live-provider adapters with redaction and cost controls.
3. Add repeated-run statistics, signed reports, and longitudinal trends.

See [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
