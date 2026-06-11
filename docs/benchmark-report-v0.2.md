# CAS Evals v0.2 Benchmark Report

**Released:** 2026-06-11  
**Evaluator:** `cas-evals 0.2.0`  
**Shared contract:** `cas-contracts v0.1.0`  
**Execution:** Deterministic local reference evaluation, no network or secrets

| Suite | Cases | Passed | Failed |
|-------|------:|-------:|-------:|
| `cas-golden-v0.2` | 8 | 8 | 0 |
| `cas-adversarial-v0.2` | 6 | 6 | 0 |

The golden corpus covers planning, implementation, debugging, Azure identity, Foundry Next Gen agents, evidence reporting, delivery, and shared contracts. The adversarial corpus covers independent secret, verification, repository, architecture, offline, and metric-safety risks.

Every per-case result conforms to the provenance-pinned published shared evaluation contract. Safety remains a mandatory independent gate and cannot be offset by other metrics.

## Reproduce

```powershell
python -m pip install -e .
.\scripts\verify.ps1
```

`python -m cas_evals.release --check` regenerates artifacts in a temporary directory and verifies byte-for-byte equality with [`releases/v0.2.0/`](../releases/v0.2.0/).
