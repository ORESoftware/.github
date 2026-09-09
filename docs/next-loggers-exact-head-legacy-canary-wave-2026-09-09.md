# next-loggers exact-head legacy consumer repair wave — 2026-09-09

Linear tracker: [DEN-3959](https://linear.app/denman/issue/DEN-3959/adopt-dual-typespec-and-json-schemaopenapi-authorities-and-enforce)

GitHub umbrella: [#159](https://github.com/ORESoftware/.github/issues/159)

Source repair PR: [ORESoftware/next-loggers.ts#41](https://github.com/ORESoftware/next-loggers.ts/pull/41)

## Why this wave exists

The 2026-09-09 `ores-otel-test` exact-head legacy consumer wave is doing its job: the shared contract phase is green for the observed Rust, Go, Dart, and Gleam canaries, while their native runtime phases expose source/API/toolchain drift. This is not a reason to weaken the test-org gate or collapse the peer-authority model. It is a bounded repair and promotion wave.

The source PR is not yet qualified for merge merely because some source-local checks are green. Promotion requires one immutable candidate source SHA to be green through source-local checks, the required TJSV convergence gate, and the exact-head native canaries. After source merge, the canaries must be repinned to the exact merged `main` SHA and rerun before their own PRs are merged.

## Exact evidence snapshot

Observed source PR head during this audit: `7389cda270dd44cba45e51050d756e810689c51e`.

Observed source workflow state at that head:

- `Context and shutdown contract`: green.
- `Server lifecycle audit`: green.
- `r2g installed consumer`: green.
- Node package-export checks: green on Node 18, 20, 22, and 24.
- `Observability hardening` run `34389154609`: red across Rust, Go, Erlang/Elixir, TypeScript contract tests, Java, and Dart.

| Lane | Canary PR | Canary head | Observed source pin | Shared contract | Native result |
| --- | --- | --- | --- | --- | --- |
| Rust | `ores-otel-test/legacy-rust-consumer#3` | `7b6d851c73b61f2419c3f688e13b40abf96cc5bc` | `94f7429a4ca61f544dd8d42ec399628e5aed0831` | green | red on native Rust formatting at exact-head run `34388788217`; PR body is stale versus branch-pinned source SHA |
| Go | `ores-otel-test/legacy-go-consumer#1` | `ab6ffd1aef8fad7cbeb8c573bc8a6c316ab8b0a5` | `d49cc63a7073c538b368adabd0899289a948417a` | green | red at run `34374864141`: `Span.IsRecording` drift, unresolved context/HTTP shutdown APIs, and CWD-dependent linter fixture paths |
| Dart | `ores-otel-test/legacy-dart-consumer#3` | `861937821ae48907882a23d2139d45b8a3234646` | `d49cc63a7073c538b368adabd0899289a948417a` | green | red at run `34374963823`: shutdown/context/logger/transport/Supabase/OTEL API drift plus missing `package:test` dev dependency |
| Gleam | `ores-otel-test/legacy-gleam-consumer#3` | `52e08740407b9399055e4f9cf790984d350bdedb` | `d49cc63a7073c538b368adabd0899289a948417a` | green | red at run `34375059759`: `gleam/erlang/process.start` is unavailable on the tested Gleam 1.15.0 / OTP 28 toolchain |

These are observed snapshots, not permanent release pins. Every promotion decision must use fresh exact-head evidence.

## Task decomposition

- [#160](https://github.com/ORESoftware/.github/issues/160) — Rust source repair and exact-head legacy certification.
- [#161](https://github.com/ORESoftware/.github/issues/161) — Go interface/context/shutdown/race/linter-fixture repair and certification.
- [#162](https://github.com/ORESoftware/.github/issues/162) — Dart shutdown/context/logger/transport/Supabase/OTEL repair and certification.
- [#163](https://github.com/ORESoftware/.github/issues/163) — Gleam process-spawn/context repair and certification.
- [#165](https://github.com/ORESoftware/.github/issues/165) — add an immutable, fail-closed TJSV convergence gate to the source/canary path.
- [#166](https://github.com/ORESoftware/.github/issues/166) — extend exact-head certification to the additional red Erlang/Elixir, TypeScript-contract, and Java lanes while retaining green Node package-export checks as positive controls.

Dedicated Linear child-issue creation is currently capacity-blocked, so these bounded GitHub workstreams remain linked to DEN-3959 and are recorded there rather than creating an untracked parallel queue.

## TJSV gap and authority rule

The inspected exact-head canary path currently shows Python `jsonschema` / fixture validation before native runtime checks. Repository search during this audit found no `typespec-json-schema-validator` or `tjsv` reference in `ORESoftware/next-loggers.ts`, and no `typespec-json-schema-validator` reference in the inspected legacy Go canary.

That Python validation remains useful independent evidence, but it is not equivalent to the required peer-authority convergence proof.

Where this contract family participates in both authored lanes:

- TypeSpec and human-authored JSON Schema/OpenAPI remain independent top-level authorities.
- TypeSpec-to-JSON-Schema or JSON-Schema-to-TypeSpec artifacts are comparison evidence only and may not silently become an authority.
- `ORESoftware/typespec-json-schema-validator` must run fail-closed from an immutable reviewed 40-character SHA.
- TJSV evidence must bind the TJSV SHA, candidate source SHA, authored-source digests, generated comparison-artifact digests, and complete declaration inventory.
- Any unexplained semantic mismatch is `STOPPED_FOR_EVALUATION` and blocks source merge, canary promotion, package release, and deployment.

If an independently authored authority lane is genuinely absent for this contract family, record that absence explicitly as an architecture gap. Do not synthesize one authority from the other merely to satisfy CI.

## Two-stage promotion sequence

1. Repair source behavior and tests semantically on the existing source repair branch, incorporating current `main` with a normal merge if synchronization is required; never rebase.
2. Select one immutable candidate source SHA.
3. Require all applicable source-local formatter, lint, unit, race/concurrency, contract, observability, and packaging checks at that exact SHA.
4. Require TJSV convergence evidence at that same candidate SHA, while retaining Python JSON Schema validation as a separate witness.
5. Repin every applicable test-org canary to that exact candidate SHA and require both the contract/TJSV path and language-native path to be green.
6. Correct PR bodies and receipts so their documented source SHA exactly matches the tested source SHA.
7. Merge the source PR only after candidate qualification is complete.
8. Repin the canaries to the exact merged `main` SHA and rerun the full gates.
9. Merge a canary PR only after its post-merge exact-head qualification is green.
10. Record final source SHA, canary workflow-head SHA, TJSV SHA, workflow run IDs, conclusions, and any intentional `STOPPED_FOR_EVALUATION` state in DEN-3959 and this ledger.

## `STOPPED_FOR_EVALUATION` conditions

Do not convert any of the following into an implicit success or a skipped green job:

- an unexplained TypeSpec versus JSON Schema/OpenAPI semantic mismatch;
- an absent required peer-authority lane;
- a cross-language API incompatibility whose intended public semantics cannot be established from contracts, history, and sibling runtimes;
- an unsupported runtime/toolchain path that lacks a semantics-preserving replacement;
- a candidate source SHA that differs from the SHA recorded in the evidence receipt;
- a mutable source or TJSV reference used as a release gate.

Each stopped state needs an exact reason, owner, evidence link, and non-bypass remediation path.

## Concurrency and preservation

Concurrent `ORESoftware/.github#164` is a separate Lambda salvage/fleet-hygiene documentation change. It does not overlap this next-loggers canary wave and must remain untouched by this branch.

Preserve open red/stale PRs and their unique tests, contracts, and implementation ideas. Do not rebase, reset, stash, force-push, rewrite history, delete branches, or choose conflict sides wholesale. Resolve any conflict semantically using the merge base, relevant history, tests, contracts, Linear context, and related repositories.
