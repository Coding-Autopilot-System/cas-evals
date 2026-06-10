# Roadmap: CAS Evals

## Phase 1: Reproducible Evaluation Kernel

**Goal:** Ship a useful, secretless v0.1 with deterministic benchmarks and evidence.

**Requirements:** BENCH-01, BENCH-02, BENCH-03, METR-01, METR-02, METR-03, METR-04, EVID-01, EVID-02, EVID-03, GOV-01, GOV-02

**Success criteria:**
1. Golden and adversarial fixtures execute identically on Windows and Linux.
2. Results contain independent quality, safety, cost, and latency evidence.
3. Test and benchmark commands pass without network access or secrets.
4. CI rejects mandatory metric failures.

## Phase 2: Shared Contracts And Corpus

Consume versioned `cas-contracts` schemas, expand representative CAS golden tasks, and publish benchmark release artifacts.

## Phase 3: Isolated Live Adapters

Add opt-in provider adapters with redaction, managed identity where applicable, cost controls, and recorded provenance.

## Phase 4: Statistical And Longitudinal Evidence

Add repeated-run statistics, baseline comparison, regression budgets, signed reports, and a public trend dashboard.
