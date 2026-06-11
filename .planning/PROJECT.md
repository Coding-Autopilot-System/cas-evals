# CAS Evals

## What This Is

CAS Evals is the public, reproducible evaluation framework for the Coding Autopilot System. It lets AI-native developers run deterministic golden tasks and adversarial prompts, then publish evidence for quality, safety, cost, and latency without requiring secrets or hosted services.

## Core Value

Every CAS capability claim can be reproduced from versioned fixtures and machine-readable results.

## Requirements

### Validated

- [x] Shared evaluation results consume provenance-pinned published `cas-contracts` schemas offline.
- [x] The public corpus represents core CAS engineering workflows and independent safety risks.
- [x] Benchmark release artifacts regenerate byte-identically with machine-readable provenance.

Validated in Phase 2: Shared Contracts And Corpus.

### Active

- [ ] Run deterministic golden-task and adversarial-prompt evaluations locally.
- [ ] Produce schema-valid quality, safety, cost, and latency evidence.
- [ ] Keep fixtures, scoring, and reports reproducible and reviewable.
- [ ] Provide CI, tests, security guidance, and contribution standards.

### Out of Scope

- Live model-provider benchmarking - v0.1 must run without secrets or network access.
- A hosted evaluation dashboard - evidence files and CI are the initial public interface.
- Provider-specific SDKs - these belong after the core contracts stabilize.

## Context

CAS needs measurable proof that its prompt refinement, autonomous engineering, and repair workflows are safe and useful. This repository is conceptually aligned with `cas-contracts`, while remaining independently runnable until shared contracts are versioned and consumed directly.

## Constraints

- **Reproducibility**: Identical fixtures and evaluator version must produce identical scores.
- **Security**: No real secrets, customer data, or remote execution in fixtures.
- **Portability**: The v0.1 core uses only the Python standard library.
- **Evidence**: Results include correlation, provenance, metric details, and pass/fail thresholds.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Standard-library Python core | Clean-machine execution and small supply-chain surface | Pending |
| JSON fixtures and result schema | Reviewable, portable, conceptually aligned with CAS contracts | Pending |
| Deterministic reference outputs | Establish reproducible baselines before live-provider evals | Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

Phase 2 is complete. The repository now consumes shared contracts offline, runs a representative v0.2 corpus, and publishes reproducible v0.2.0 release evidence. Phase 3 adds isolated opt-in live adapters.

After each phase, validate requirements, record new decisions, and update scope. After each milestone, review the core value, exclusions, and evidence quality.

---
*Last updated: 2026-06-11 after Phase 2 completion*
