# CAS Evals v0.1 Benchmark Report

**Evaluated:** 2026-06-11  
**Evaluator:** `cas-evals 0.1.0`  
**Execution:** Deterministic local reference evaluation, no network or secrets

| Suite | Cases | Passed | Failed |
|-------|------:|-------:|-------:|
| `cas-golden-v0.1` | 2 | 2 | 0 |
| `cas-adversarial-v0.1` | 2 | 2 | 0 |

All cases passed independent quality, safety, cost, and latency gates. Safety is mandatory and cannot be offset by other metrics.

## Reproduce

```powershell
python -m pip install -e .
.\scripts\verify.ps1
```

Generated evidence is written to `artifacts/` and intentionally excluded from source control. Each result records the exact fixture SHA-256 digest.
