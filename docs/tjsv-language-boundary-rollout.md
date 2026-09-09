# TJSV language-boundary rollout and evidence hardening

Tracking: Linear `DEN-3830`; GitHub parent [`ORESoftware/.github#36`](https://github.com/ORESoftware/.github/issues/36).

Last reconciled: 2026-09-09.

## Baseline

`ORESoftware/typespec-json-schema-validator#71` merged the fail-closed language/runtime boundary verifier to `main` as `dfc28bfc000faba5a963f23c708171dfd5f8debf`. Its exact PR head and the merged `main` revision both completed the repository's Ubuntu 24.04 and macOS 14 gates, including production dependency audit, syntax and flags-2-env checks, unit and compiler-backed integration tests, package-boundary checks, and clean-consumer acceptance.

This is the baseline for this roadmap, not a claim that all downstream languages, transports, binaries, emitters, or repositories are certified.

## Non-negotiable authority model

- TypeSpec and independently authored JSON Schema/OpenAPI are peer editable authorities.
- TypeSpec-generated JSON Schema is comparison evidence only.
- Contract IR, runtime evidence, Protobuf/WIT, generated clients, SQL/ORM projections, build outputs, canary receipts, and admission receipts are downstream evidence.
- No generated artifact may overwrite either authored authority or win a disagreement by fallback.
- Any unexplained mismatch is `STOPPED_FOR_EVALUATION` and blocks the promotion step that depends on it.
- A lower-level `passed` receipt never implies stronger claims such as live transport coverage, reproducible binaries, deployment success, or fleet-wide coverage unless the named assurance profile requires and verifies that evidence.

## Why GitHub issues are the executable backlog

The Linear workspace currently rejects new issue creation because it has reached its issue-count limit. Existing DEN issues remain the cross-system planning context. New bounded implementation tasks therefore live in their owning GitHub repositories and are mirrored into the Linear project document **TJSV language-boundary rollout work breakdown — DEN-3830 — 2026-09-09**.

Do not infer that a GitHub issue is untracked merely because a dedicated Linear child cannot currently be created.

## Ownership boundaries

| Area | Primary owner | Existing tracker | Boundary |
| --- | --- | --- | --- |
| Peer-authority parity, Contract IR, runtime-boundary admission | `ORESoftware/typespec-json-schema-validator` | DEN-3830; validator issues | Validator verifies evidence; it does not own every emitter. |
| Operation/API IR, Protobuf, gRPC/Connect, tRPC and downstream generation | `ORESoftware/api-docs` | [`api-docs#38`](https://github.com/ORESoftware/api-docs/issues/38) | Generated projections consume admitted IR and explicit operation metadata. |
| Reusable/fleet policy, assurance profiles and promotion rules | `ORESoftware/.github` | [#36](https://github.com/ORESoftware/.github/issues/36) | Account-level policy must not duplicate validator or emitter implementation. |
| Fleet discovery and diagnostics | `ORESoftware/ores-cli`, `ores-gh-bots` | DEN-3043 and `.github` fleet issues | Audit reports evidence; it does not become a new parity engine. |
| Cross-language consumer/runtime matrices | target `*-clients`, `*-interfaces`, `*-test` repos | DEN-3406, DEN-3958, DEN-2273, DEN-3959 | Native consumers must execute real validation/codec paths at exact revisions. |

## Newly discovered validator-local gaps

### 1. Reverify language-boundary admission against current inputs

[`ORESoftware/typespec-json-schema-validator#78`](https://github.com/ORESoftware/typespec-json-schema-validator/issues/78)

The pure verifier must remain reusable, but trusted promotion needs a file/current-workspace entrypoint that reuses TJSV's canonical parity and Contract-IR verification path. It must recompute current source closure and reject passed-looking but forged/stale report or IR objects before runtime artifacts can be admitted.

This is a prerequisite for treating the boundary API as a promotion authority in reusable CI.

### 2. Keep public Draft 2020-12 evidence schemas and executable behavior in lockstep

[`ORESoftware/typespec-json-schema-validator#79`](https://github.com/ORESoftware/typespec-json-schema-validator/issues/79)

The manifest, evidence, and verification-receipt schemas are public cross-runtime wire contracts. Add an independent Draft 2020-12 conformance corpus so structurally invalid envelopes cannot be accepted by the JavaScript path and every emitted decision validates against the published receipt schema. Cross-object semantic constraints remain explicit runtime policy where JSON Schema cannot or should not encode them.

## Existing post-merge backlog — compose, do not duplicate

Parent program: [#36](https://github.com/ORESoftware/.github/issues/36).

- [#37](https://github.com/ORESoftware/.github/issues/37) — package language-boundary verification as canonical reusable pinned CI admission.
- [#38](https://github.com/ORESoftware/.github/issues/38) — add live HTTP/WebSocket/browser boundary evidence above parsed-value receipts.
- [#40](https://github.com/ORESoftware/.github/issues/40) — bind stronger profiles to reproducible-build and executable provenance.
- [#41](https://github.com/ORESoftware/.github/issues/41) and [#44](https://github.com/ORESoftware/.github/issues/44) — exact-head `*-test` canary promotion and machine-readable canary receipts.
- [#43](https://github.com/ORESoftware/.github/issues/43) — add Go and Gleam native consumers.
- [#46](https://github.com/ORESoftware/.github/issues/46) — qualify evidence by OS, architecture and WASM target.
- [#54](https://github.com/ORESoftware/.github/issues/54) — define named assurance profiles and bounded claim vocabulary.
- [#55](https://github.com/ORESoftware/.github/issues/55) — automate safe immutable validator/toolchain/receipt-schema upgrades.
- [#57](https://github.com/ORESoftware/.github/issues/57) — gate package, release and deployment promotion on current required receipts.
- [#60](https://github.com/ORESoftware/.github/issues/60) — aggregate exact evidence into a non-vacuous fleet ledger.
- [#63](https://github.com/ORESoftware/.github/issues/63) — mutation, fuzz and vacuity resistance.
- [#65](https://github.com/ORESoftware/.github/issues/65) — compare normalized accepted output and stable error evidence, not verdicts only.
- [#68](https://github.com/ORESoftware/.github/issues/68) — prove tri-state PATCH missing/null/value semantics.
- [#78](https://github.com/ORESoftware/.github/issues/78), [#79](https://github.com/ORESoftware/.github/issues/79), [#80](https://github.com/ORESoftware/.github/issues/80) — shared-interface skew diagnostics, fleet validator inventory and five-primary-runtime certification.

Broad existing Linear work remains complementary: DEN-3043, DEN-3406, DEN-3958, DEN-3959, DEN-2273, DEN-3982, DEN-3828, and DEN-3830.

## Additional account-level tasks discovered in this reconciliation

- [#95](https://github.com/ORESoftware/.github/issues/95) — keep this roadmap, validator issues and Linear document synchronized.
- [#97](https://github.com/ORESoftware/.github/issues/97) — audit the task graph for duplicate, superseded or complementary work before expanding it.
- [#99](https://github.com/ORESoftware/.github/issues/99) — define evidence retention, staleness, expiry and historical-pass semantics shared by release/fleet tooling.
- [#100](https://github.com/ORESoftware/.github/issues/100) — make dependency/blocker edges explicit instead of relying on issue-title inference.
- [#101](https://github.com/ORESoftware/.github/issues/101) — define public-safe redaction/allowlist policy for fleet and release evidence.
- [#103](https://github.com/ORESoftware/.github/issues/103) — keep roadmap completion distinct from implementation, exact-head CI, merge, canary and rollout completion.
- [#105](https://github.com/ORESoftware/.github/issues/105) — require duplicate search and ownership review before creating more TJSV rollout issues.
- [#107](https://github.com/ORESoftware/.github/issues/107) — impose a task-creation budget on future exploratory rollout audits.

These are governance/coordination tasks. They must not be mistaken for completion of the implementation they track.

## Critical path

### Phase A — stabilize the admission contract

1. **Validator #79** — public evidence-schema versus executable-behavior conformance.
2. **Validator #78** — canonical current-input and Contract-IR re-verification.
3. **Account #63** — non-vacuity, mutation and bounded fuzzing over the now-stable entrypoints.
4. **Account #54** — version assurance profiles and permitted claim vocabulary.

Exit: the base `runtime-boundary` profile has one reviewed grammar, one canonical current-input admission path, adversarial negative controls, and explicit claim limits.

### Phase B — make the gate reusable and execute real native evidence

5. **Account #37** — publish pinned reusable CI around the canonical current-input API.
6. **Account #65 / #68** — strengthen runtime semantics beyond verdict equality and cover missing/null/value update semantics.
7. **Account #43 / #80 + DEN-3406 / DEN-2273** — execute the primary Rust, TypeScript/Node, Dart/Flutter, Go and Gleam/BEAM runtime matrix where supported.
8. **Account #46** — qualify required runtime evidence by platform/architecture/WASM target rather than letting Linux stand in for every target.
9. **`api-docs#38`** — continue downstream API/transport projection generation from admitted IR; do not move emitter ownership into TJSV.

Exit: reusable CI produces exact, non-vacuous, platform-qualified runtime evidence for named supported targets and fails closed on skipped/unsupported mandatory cells.

### Phase C — prove stronger external boundaries

10. **Account #38** — real HTTP/WebSocket/browser/server evidence.
11. **Account #40** — reproducible build and executable provenance where a profile requires it.
12. **Account #41 / #44** — exact-head test-org canaries and canonical canary receipts.

Exit: stronger profiles can distinguish parsed-value evidence from live transport and binary provenance without overclaiming.

### Phase D — make evidence operational

13. **Account #99 / #101 / #103** — settle freshness, retention, redaction and state vocabulary before durable aggregation.
14. **Account #57** — enforce required profiles at package/release/deployment promotion.
15. **Account #60** — aggregate exact evidence into the fleet ledger.
16. **Account #55 / #78 / #79** — safe immutable upgrade PRs plus fleet skew/validator-gap diagnostics.
17. **Account #100 / #97 / #105 / #107** — keep dependency, deduplication and backlog-creation discipline machine-readable.

Exit: a release or fleet summary cannot become green from stale, missing, zero-step, private-data-leaking, wrong-commit, wrong-profile or wrong-artifact evidence.

## Stop conditions shared by every phase

- A workflow file exists but the required job did not execute.
- A required job is skipped, zero-step, cancelled, runner-blocked or missing.
- The source commit, validator revision, assurance profile, Contract IR, runtime target or artifact differs from the evidence being used.
- Current authored TypeSpec or JSON Schema/OpenAPI differs from the closure used to generate the receipt.
- A required native runtime/platform/transport is unsupported but represented as passed instead of explicitly refused/unsupported.
- A receipt contains private/customer/secret-bearing material that violates its public evidence policy.
- A newer source/profile/toolchain makes an old receipt historical or stale under the active policy.
- A generated projection attempts to become an editable authority or to repair an authored source.
- An unexplained semantic disagreement is present anywhere in the required assurance profile.

## Status vocabulary

Roadmap and fleet reporting should distinguish at least:

- `planned`
- `implemented`
- `exact_head_ci_passed`
- `merged`
- `post_merge_verified`
- `canary_passed`
- `rollout_complete`
- `blocked`
- `failed`
- `unsupported`
- `missing`
- `zero_step`
- `stale`
- `expired`
- `historical_pass`
- `stopped_for_evaluation`

Do not collapse these into one green checkbox.

## Evidence safety

Public receipts and dashboards should contain only bounded, public-safe metadata needed to verify the claim: exact public-safe repo/commit identity, validator/profile/toolchain identifiers, digests, counts, stable rule IDs, workflow/job references and explicit limitations. Do not publish raw rejected instances, source bodies, broad environment dumps, credentials, customer identifiers, private repository inventories, private paths, or secret-bearing argv/logs.

Private diagnostic evidence may be referenced through an approved private store/channel; the public record should contain the reference and bounded status, not the private payload.

## Synchronization rules

- GitHub issues are the executable backlog while Linear child creation is blocked by the workspace issue cap.
- DEN-3830 remains the primary Linear context; the Linear project document mirrors this roadmap.
- `ORESoftware/.github#36` remains the account-level parent program.
- Validator implementation stays in `typespec-json-schema-validator`; emitter implementation stays in `api-docs` or the target producer; fleet diagnostics stay in `ores-cli`/`ores-gh-bots`.
- Before creating any new task, search existing GitHub and Linear work and classify the proposal as `new`, `covered`, `superseded`, or `complementary`.
- Never auto-close/delete older issues during reconciliation; link or comment unless a human explicitly authorizes closure.
- A roadmap/doc PR proves documentation only. It does not advance implementation state without exact implementation evidence.
