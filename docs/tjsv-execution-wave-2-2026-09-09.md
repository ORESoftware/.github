# TJSV execution wave 2 — Rust-first and evidence hardening

Status: active, 2026-09-09  
Parent program: [`ORESoftware/.github#36`](https://github.com/ORESoftware/.github/issues/36)  
Primary Linear context: `DEN-3830`, `DEN-3959`

This is a companion execution ledger to [the TJSV language-boundary admission rollout roadmap](./tjsv-language-boundary-admission-roadmap.md). It records residual work discovered after the initial roadmap, validator, consumer, Linear, and stale-branch audit. It does not replace the original backlog; it adds bounded implementation slices that were not already owned by the reusable-CI, live-transport, provenance, platform, release, fleet-ledger, upgrade, or mutation tasks.

## Audit snapshot

The planning audit used these exact observed revisions:

- `ORESoftware/typespec-json-schema-validator@4740f1367a7906813dcd420a77d0c9ede26943fb`;
- `ORESoftware/api-docs@0afc518e6329f451b5401551ada6452607f0f089`;
- stale `ORESoftware/api-docs#36` branch `wip/land-uncommitted-20260906`, which was 235 commits behind current main and 2 commits ahead from merge base `18329bdd2ea2082fea6319651b620c7868c6959d`.

Those SHAs are planning evidence, not a rule that every consumer must always use the current upstream default branch. Consumer admission continues to require an exact reviewed validator/profile revision appropriate to its declared assurance profile.

The `api-docs` source audit also found a large operational Python surface across route generation and synchronization, peer-authority checks, RPC IDL audits, projection generation, generated-tree checks, bundle creation, sibling-reference resolution, and documentation sweeps. That implementation inventory motivates the Rust-first parity migration below; it is not evidence that Python behavior may be discarded.

## New executable tasks

| Priority | GitHub issue | Work package | Required outcome |
| --- | --- | --- | --- |
| P0 | [`#77`](https://github.com/ORESoftware/.github/issues/77) | Single TJSV consumer lock and pin-drift gate | Workflows, runtime constants, policies, receipt schemas, toolchain ledgers, and documentation agree with one reviewed exact-pin manifest. |
| P0 | [`#81`](https://github.com/ORESoftware/.github/issues/81) | Resource-bounded admission | Schemas, reference graphs, corpora, reports, child processes, logs, concurrency, and temporary storage cannot cause unbounded or false-green evaluation. |
| P0 | [`#73`](https://github.com/ORESoftware/.github/issues/73) | Rust-first `api-docs` CLI migration | Python operational CLIs move to modular Rust only after Python-vs-Rust semantic, output, exit-code, and failure-class parity. |
| P0 | [`#93`](https://github.com/ORESoftware/.github/issues/93) | Semantic salvage of stale `api-docs#36` | Every old changed path receives a disposition; unique work is reconstructed on current main without wholesale branch merge or closure of the historical draft. |
| P1 | [`#85`](https://github.com/ORESoftware/.github/issues/85) | Backward/forward contract evolution | Same-version peer parity is augmented with directional old/new client, server, stored-payload, event, descriptor, and runtime compatibility evidence. |
| P1 | [`#88`](https://github.com/ORESoftware/.github/issues/88) | HTTP response/error/metadata peer surface | Independently authored TypeSpec and Draft 2020-12 peers cover parsed response variants, public errors, typed metadata, and generated runtime consumers. |
| P1 | [`#90`](https://github.com/ORESoftware/.github/issues/90) | Independent validator diversity | High-assurance profiles execute the same authored schema/corpus through multiple genuine implementation lineages; any required verdict disagreement stops evaluation. |

## Dependency order

### Foundation: define and bind what is being proved

1. Stabilize named assurance profiles and claim vocabulary in [`#54`](https://github.com/ORESoftware/.github/issues/54), plus the validator-local public-schema/current-input work tracked in TJSV issues #79 and #78.
2. Package the canonical reusable exact-input boundary in [`#37`](https://github.com/ORESoftware/.github/issues/37).
3. Add the repo-local exact-pin/profile lock in `#77` and bounded execution in `#81`.

### Implementation: remove accidental toolchain fragmentation

4. Inventory and migrate the operational Python surface under `#73`. Keep Python as the differential oracle until each Rust command proves parity. Public flags belong in root `.cli-flags.toml` and are parsed through `flags-2-env`; no parallel argument authority is allowed.
5. Audit stale `api-docs#36` under `#93` in parallel. Reuse current implementations where the old intent is already integrated, recover only unique behavior, and route still-useful Python-only behavior into the Rust parity plan.

### Contract strength: add missing temporal and output boundaries

6. Add parsed HTTP response/error/metadata admission under `#88`; then use [`#38`](https://github.com/ORESoftware/.github/issues/38) for the separate raw HTTP/WebSocket/browser/live-server layer.
7. Add directional contract-evolution profiles under `#85`, building on `#54` and feeding release qualification in [`#57`](https://github.com/ORESoftware/.github/issues/57).
8. Add independent validator lineages under `#90`, after bounded execution is available. Coordinate vacuity and hostile-case generation with [`#63`](https://github.com/ORESoftware/.github/issues/63).

### Fleet operation: qualify, aggregate, and block promotion

9. Continue runtime-observation, Go/Gleam, OS/architecture/WASM, live-transport, and binary-provenance work in `#43`, `#46`, `#38`, `#40`, `#63`, and the related semantic-observation tasks.
10. Aggregate exact-current evidence in [`#60`](https://github.com/ORESoftware/.github/issues/60).
11. Make package, release, and deployment promotion consume the exact required profile under `#57`.
12. Use [`#55`](https://github.com/ORESoftware/.github/issues/55) for future immutable validator/profile/toolchain upgrade PRs after the lock contract exists.

## Non-negotiable authority and evidence model

- Human-authored TypeSpec and human-authored JSON Schema/OpenAPI remain independent peer top-level authorities.
- Generated Schema B, Contract IR, operation IR, Protobuf/WIT, generated clients, lock manifests, compatibility baselines, runtime observations, validator matrices, reports, documentation, and receipts remain projections or evidence.
- No source, generator, runtime, validator, language, old branch, or receipt wins by fallback.
- Missing, stale, unsupported, zero-step, conflicting, over-budget, incomplete-profile, or differently bound required evidence cannot be reported as passed.
- Same-version parity does not imply backward compatibility; parsed-value evidence does not imply live transport; runtime observations do not imply reproducible builds; one platform does not imply another; one validator lineage does not imply independent corroboration.
- Historical receipts and branches remain historical evidence. They do not automatically certify current main and are not rewritten to look current.

## Git and conflict rules

- Start implementation work from current target-branch heads and include the relevant `DEN-<n>` in branch names and PR titles.
- Resolve conflicts semantically using current source, tests, history, specifications, and sibling implementations. Never use blanket `ours` or `theirs` selection.
- Preserve all unique work. Do not rebase, reset, stash, force-push, or close the stale draft merely to make the graph look clean.
- Stage explicit paths, scan for conflict markers, and run the complete affected exact-head formatter, linter, TJSV, authority, generated-contract, runtime, and language gates before merge.
- Keep credentials out of arguments, files, logs, receipts, comments, and documentation. No token rotation or revocation is part of this program.

## Linear synchronization

The canonical Linear document is **TJSV language-boundary rollout work breakdown — DEN-3830 — 2026-09-09** in project `github.com/ORESoftware`. This execution wave is appended there and summarized on both `DEN-3830` and `DEN-3959`.

The Linear workspace currently rejects new child issues because the issue-count limit is exhausted. These GitHub issues are therefore the executable task records. The Linear document and existing DEN trackers provide cross-system status, decisions, and evidence without fabricating identifiers or losing the work.

## Completion criteria for this wave

This wave is complete only when:

1. adopted consumers have one verified exact-pin/profile lock and bounded evaluation;
2. each migrated Rust command proves differential parity before replacing a Python CI call site;
3. the stale draft has a complete path disposition and every unique safe behavior is either landed or explicitly awaiting an owner decision;
4. response/error and temporal compatibility evidence run against real runtime consumers;
5. high-assurance profiles execute the declared independent validator lineages and stop on disagreement;
6. exact-current receipts flow into the fleet ledger and promotion gates without overstating the evidence layer actually proved.
