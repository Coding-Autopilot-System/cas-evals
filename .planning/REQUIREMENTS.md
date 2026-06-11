# Requirements: CAS Evals

**Defined:** 2026-06-11
**Core Value:** Every CAS capability claim can be reproduced from versioned fixtures and machine-readable results.

## v1 Requirements

### Benchmarks

- [ ] **BENCH-01**: Maintainer can define golden tasks as reviewable JSON fixtures.
- [ ] **BENCH-02**: Maintainer can define adversarial prompts with explicit safe expected outcomes.
- [ ] **BENCH-03**: Evaluator records a fixture digest so evidence can be correlated to exact inputs.

### Metrics

- [ ] **METR-01**: User receives deterministic quality evidence from expected keywords.
- [ ] **METR-02**: User receives safety evidence from prohibited content checks.
- [ ] **METR-03**: User receives normalized cost evidence and threshold status.
- [ ] **METR-04**: User receives latency evidence and threshold status.

### Evidence

- [ ] **EVID-01**: User can emit contract-aligned JSON evaluation results.
- [ ] **EVID-02**: User can reproduce identical results from identical fixtures.
- [ ] **EVID-03**: CI fails when any mandatory evaluation gate fails.

### Governance

- [ ] **GOV-01**: Contributor can run documented tests and benchmarks without secrets.
- [ ] **GOV-02**: Repository publishes security and contribution guidance.

### Shared Contracts And Corpus

- [ ] **SHRD-01**: Maintainer can validate emitted evaluation results against a provenance-pinned published `cas-contracts` schema without network access.
- [ ] **CORP-01**: User can run a representative golden-task corpus covering core CAS engineering workflows.
- [ ] **REL-01**: Maintainer can deterministically generate and publish reviewable benchmark release artifacts.

## v2 Requirements

- **LIVE-01**: User can evaluate live model-provider responses through isolated adapters.
- **STAT-01**: User can compute confidence intervals over repeated non-deterministic runs.
- **DASH-01**: User can inspect longitudinal benchmark trends in a public dashboard.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Hosted model calls | v0.1 must be secretless and deterministic |
| Autonomous code execution | Requires a separate isolation and policy design |
| Composite score hiding safety failures | Safety must remain an independent mandatory gate |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| BENCH-01, BENCH-02, BENCH-03 | Phase 1 | Complete |
| METR-01, METR-02, METR-03, METR-04 | Phase 1 | Complete |
| EVID-01, EVID-02, EVID-03 | Phase 1 | Complete |
| GOV-01, GOV-02 | Phase 1 | Complete |
| SHRD-01, CORP-01, REL-01 | Phase 2 | Pending |

**Coverage:** 15 v1 requirements, 15 mapped, 0 unmapped.

---
*Last updated: 2026-06-11 after v0.1 scaffold*
