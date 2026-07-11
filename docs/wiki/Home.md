# CAS Evals Wiki

## Role in the CAS portfolio

`cas-evals` is part of the **Governance plane** of the Coding-Autopilot-System three-plane
model (Control / Execution / Governance). It is the evidence gate: it runs versioned golden
and adversarial tasks against deterministic reference responses (or, opt-in, against a live
`cas-reference-product` workflow) and produces machine-readable, schema-conformant
quality/safety/cost/latency evidence with a CLI that exits non-zero on any mandatory metric
failure — making "done" mean something checkable, not just claimed.

| Plane | This repo's responsibility |
|---|---|
| Control | *(consumed indirectly — evidence gate for control-plane goal completion)* |
| Execution | *(consumed indirectly — evaluates `cas-reference-product` live output, opt-in)* |
| Governance | Deterministic evaluation kernel, evidence gate, `cas-contracts` schema validation |

## Quickstart

- [README.md](../../README.md) — Quickstart, Metrics, Evidence Contract
- [Architecture](./Architecture.md) — evidence gate flow (offline + live reference-product modes)
- [Operations](./Operations.md) — verified CLI/gate/CI commands
- [Decisions](./Decisions.md) — phase history and open PRs (including the registry-fetch
  smoke check, PR #9)

## Ecosystem links

Part of the [Coding-Autopilot-System](https://github.com/Coding-Autopilot-System) org:
[gsd-orchestrator](https://github.com/Coding-Autopilot-System/gsd-orchestrator) (control plane) ·
[autogen](https://github.com/Coding-Autopilot-System/autogen) (execution plane) ·
[Promptimprover](https://github.com/Coding-Autopilot-System/Promptimprover) (prompt governance) ·
[cas-contracts](https://github.com/Coding-Autopilot-System/cas-contracts) (shared schemas)

<!-- docs-verified: 4fe936cc83ffdc4fd6ad825c373e949b1edbe0eb 2026-07-08 -->
