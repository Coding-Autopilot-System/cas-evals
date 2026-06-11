# Phase 2 Research: Shared Contracts And Corpus

## Findings

- `cas-contracts` published tag `v0.1.0` on 2026-06-10 with no attached release assets.
- The authoritative evaluation contract is `schemas/v0.1/evaluation-result.schema.json` and references `common.schema.json`.
- The shared result contract requires lifecycle metadata, W3C trace context, evaluator identity, outcome, and numeric metrics.
- The shared contract rejects unevaluated properties, so CAS-specific threshold details must live outside each shared result object.
- Runtime downloads would break reproducibility and standalone execution. Vendoring immutable tagged schemas with verified provenance is the durable offline approach.

## Risks And Mitigations

| Risk | Mitigation |
|------|------------|
| Vendored schema drift | Verify exact SHA-256 digests and published blob SHAs in tests. |
| Partial schema validation | Implement and test the shared contract's complete current constraint surface. |
| Safety hidden by aggregate scores | Preserve a separate safety metric and mandatory pass decision. |
| Non-reproducible releases | Sort JSON keys, use fixed fixture metadata, and verify regeneration is byte-identical. |

---

*Researched: 2026-06-11*
