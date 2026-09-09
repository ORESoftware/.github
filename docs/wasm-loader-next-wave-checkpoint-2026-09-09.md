# OWLS next-wave live execution checkpoint — 2026-09-09

Canonical plan: [`wasm-loader-next-wave-2026-09-09.md`](./wasm-loader-next-wave-2026-09-09.md)  
Linear umbrella: `DEN-3959`  
Linear projects: `ores-wasm-loaders`, `ores-wasm-loaders-test`

This checkpoint maps the canonical WL/WT backlog to concrete GitHub tasks and current execution evidence. It is not a second plan, contract authority, or rollout approval.

## Current contract generation

- TJSV: `03ccc0ecdfc70f9198c3ccf80718910961d3fde1`
- interfaces dependency-DAG contract: `cfe0b18fe9ae361d94ea0646627cb732465b5496`
- browser loader dependency-aware route preparation: `d9f7624c80b606e8be5479f9e2dea89ac9e35284`
- native DAG-compatible merged head: `1cbd6107b26e85420b924afa9cae1d401e223802`; exact-head run `34388127745` passed
- Flutter DAG-compatible merged head: `8f6bda35d8efb21b817295b01e4b0c58a59910cd`; exact-head run `34388363929` passed
- prior independent five-host closure: `owls-e2e@c9a01743f554c126f04231b8da38c4a59d265390`; preserve as historical evidence until refreshed to the DAG generation

Native duplicate PR `owls-runtime.rs#10` was closed after the equivalent mainline DAG admission landed and passed. Flutter PR `owls-flutter#8` merged normally after all three package/admission/compatibility jobs passed.

## Concrete GitHub task mapping

| Canonical work | GitHub task | State at this checkpoint |
| --- | --- | --- |
| WL-17 native DAG propagation | `.github#102` | implemented by native main `1cbd6107...` |
| WL-17 Flutter DAG propagation | `.github#104` | merged by `owls-flutter#8` -> `8f6bda35...` |
| WL-17 five-host closure refresh | `.github#106` | next P0; use merged native/Flutter DAG heads |
| WL-18 + WT-09 real Dioxus emitted split graph | `.github#108` | active independent implementation also exists as `owls-e2e#12`; do not duplicate it |
| WL-19 route-intent integration | `.github#118` | open |
| WL-20 immutable remote publication/portable locks | `.github#110` | open |
| WL-21 + WT-13/14 telemetry/field evidence | `.github#111` | open |
| WL-22 adaptive bounded speculation | `.github#119` | open |
| WL-23/25 + WT-10/12 origin/security/mobile qualification | `.github#112` | open |
| WL-24 atomic release selection/long-lived tabs | `.github#121` | open |
| WT-11 persistent-shell lifecycle soak | `.github#123` | open |
| WT-15/16 rollback + staged rollout decision | `.github#113` | open |
| WL-26 read-only `oresc` fleet audit | `.github#124` | open |

Task URLs:

- https://github.com/ORESoftware/.github/issues/102
- https://github.com/ORESoftware/.github/issues/104
- https://github.com/ORESoftware/.github/issues/106
- https://github.com/ORESoftware/.github/issues/108
- https://github.com/ORESoftware/.github/issues/110
- https://github.com/ORESoftware/.github/issues/111
- https://github.com/ORESoftware/.github/issues/112
- https://github.com/ORESoftware/.github/issues/113
- https://github.com/ORESoftware/.github/issues/118
- https://github.com/ORESoftware/.github/issues/119
- https://github.com/ORESoftware/.github/issues/121
- https://github.com/ORESoftware/.github/issues/123
- https://github.com/ORESoftware/.github/issues/124

## Immediate dependency order

1. Treat native/Flutter host DAG propagation as complete only from their merged exact-head evidence above.
2. Refresh `ores-wasm-loaders-test/owls-e2e` to one immutable five-host DAG closure (#106). This may proceed in parallel with the isolated real-Dioxus PR because `owls-e2e#12` changes only its dedicated Dioxus workflow/fixture files.
3. Merge real-Dioxus evidence only after all required exact-head workflows pass; do not infer host closure promotion from that lane.
4. Route-intent integration (#118) should consume the admitted dependency graph and real-Dioxus evidence rather than guess split filenames.
5. Publication, telemetry, adaptive policy, topology/security/mobile, atomic release, lifecycle soak, rollback and fleet audit remain independent acceptance lanes. A green lane never substitutes for another.

## Invariants

- TypeSpec and hand-authored JSON Schema Draft 2020-12 remain independent editable peer authorities with no precedence.
- `ORESoftware/typespec-json-schema-validator` remains the required exact, immutable convergence/admission boundary.
- Generated Schema B, Contract IR, language projections and receipts are evidence only.
- Keep released-package provenance separate from current-head compatibility until publication actually occurs.
- Preserve old receipts/source closures additively; do not rewrite historical evidence.
- No rebase, stash, reset, force-push, or shallow conflict-side selection. Merge concurrent default-branch work semantically and rerun exact-head gates.
- No credential from chat, repository history or issue text is a credential fallback. Do not revoke/rotate credentials without explicit authorization.
- No automatic artifact/test result authorizes the 35+ organization production rollout; rollout requires the explicit staged decision gate.
