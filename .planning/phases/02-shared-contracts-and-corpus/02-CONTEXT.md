# Phase 2: Shared Contracts And Corpus - Context

**Gathered:** 2026-06-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Consume the published `cas-contracts` v0.1.0 evaluation schema, expand representative CAS golden tasks, and publish deterministic benchmark release artifacts while preserving secretless, network-free execution.

</domain>

<decisions>
## Implementation Decisions

### Shared contract consumption
- Vendor the exact schemas published under the immutable `cas-contracts` tag `v0.1.0`.
- Record source URLs, tag, blob SHAs, and file SHA-256 digests.
- Validate provenance and emitted `EvaluationResult` objects using only Python's standard library.
- Never download schemas during evaluator, test, benchmark, or release execution.

### Evidence model
- Make every per-case result conform exactly to the shared `EvaluationResult` schema.
- Keep threshold and violation details in the surrounding suite evidence envelope.
- Keep safety as an independent mandatory gate.

### Corpus and releases
- Expand the golden corpus across planning, implementation, debugging, security, Azure identity, and evidence reporting.
- Generate checked-in release artifacts deterministically from versioned fixtures.
- Include fixture and artifact digests in a machine-readable release manifest.

</decisions>

<canonical_refs>
## Canonical References

- `.planning/PROJECT.md` - Core value and offline constraints.
- `.planning/REQUIREMENTS.md` - Phase requirement IDs.
- `.planning/ROADMAP.md` - Phase boundary.
- `AGENTS.md` - Mandatory evaluator and verification rules.
- `https://github.com/Coding-Autopilot-System/cas-contracts/releases/tag/v0.1.0` - Published shared-contract release.

</canonical_refs>

<deferred>
## Deferred Ideas

- Live provider adapters remain Phase 3.
- Statistical and longitudinal analysis remains Phase 4.

</deferred>

---

*Phase: 02-shared-contracts-and-corpus*
*Context gathered: 2026-06-11*
