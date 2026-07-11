# Decisions

## ADR convention

`docs/adr/README.md` establishes the convention (sequential numbering, Context/Decision/
Consequences) but **no numbered ADR files exist in the repo yet**. Decisions to date live in
`.planning/phases/` plan/summary pairs instead.

## Phase history (`.planning/phases/`, this repo's own GSD project)

| Phase | Topic |
|---|---|
| 02 | Shared contracts and corpus |

See `.planning/phases/02-shared-contracts-and-corpus/*-SUMMARY.md` for the detailed record.

## Open decisions tracked in this Phase 36 refresh

- **PR #9** (`feat/registry-fetch-smoke-check`) — adds a live registry-fetch smoke check
  (`cas_evals.registry_check`) and re-vendors `$id` expectations to the resolvable Pages URL
  convention, as a companion to `cas-contracts` PR #18; open, not yet merged. See
  [Architecture](./Architecture.md#registry-fetch-smoke-check--in-progress-pr-9).
- **PR #10** (`ci/sha-pin-actions`) — pins third-party GitHub Actions to commit SHAs; open,
  not yet merged. (Note: the current `ci.yml` already shows pinned `checkout`/`setup-python`
  actions on `main` — verify PR #10's remaining scope before assuming no pinning exists.)

<!-- docs-verified: 4fe936cc83ffdc4fd6ad825c373e949b1edbe0eb 2026-07-08 -->
