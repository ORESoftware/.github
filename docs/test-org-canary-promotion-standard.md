# Test-org exact-head canary promotion standard

Status: proposed account-level standard under [DEN-3959](https://linear.app/denman/issue/DEN-3959/adopt-dual-typespec-and-json-schemaopenapi-authorities-and-enforce).

Tracking issues: [#41](https://github.com/ORESoftware/.github/issues/41) and [#44](https://github.com/ORESoftware/.github/issues/44).

## Purpose

Sibling `*-test` GitHub organizations are isolated downstream witnesses for changes that cross repository, contract, language, runtime, package, or deployment boundaries. They are not generated mirrors and they are not permission to weaken production gates. Their job is to prove that one immutable candidate source/tool revision is consumable by independent downstream harnesses before promotion.

The first concrete implementation was exercised on 2026-09-09 in `ores-otel-test`: canonical and legacy logging consumers were advanced to immutable source heads across Node, Rust, Go, Dart, and Gleam. The run demonstrated why this layer matters: contract validation passed on every legacy runtime while native Rust, Go, Dart, and Gleam execution exposed distinct source defects.

## Required lifecycle

1. **Select immutable candidates.** Record production source repository + 40-character commit SHA and every validator/generator/tool SHA that affects admission. Never use a mutable branch as evidence.
2. **Preserve independent authorities.** TypeSpec and independently authored JSON Schema/OpenAPI remain peer editable authorities. Generated TypeSpec→JSON Schema or reverse translations are evidence only.
3. **Bind the test harness.** Update checked-in test evidence so it names the exact production source/tool heads under test. The test repository head is itself immutable evidence once CI starts.
4. **Run independent gates.** Contract parity/admission and native runtime consumer execution are separate required witnesses. A contract pass never implies runtime success.
5. **Treat absence as failure.** Missing, queued, skipped, canceled, zero-step, runnerless, stale, or otherwise non-executed required jobs are not green evidence.
6. **Keep red canaries visible.** Diagnose the authoritative source. Do not delete tests, weaken assertions, change an exact SHA to a mutable ref, or rewrite the downstream harness merely to obtain green CI.
7. **Repair source, then repoint.** Publish a focused source repair branch/PR. Repoint the existing red canary to the exact repair commit and rerun the same native + contract gates.
8. **Promote only exact tested heads.** Merge/release/promote production only when every required canary is green for the same exact candidate source/tool closure. Re-check that production main and PR heads have not advanced.
9. **Requalify the merged production head.** After a source PR merges, repoint required canaries to the exact merged `main` SHA and rerun the required admission + native gates before merging the canary PRs. A pre-merge PR-head receipt is not evidence for a different merge commit.
10. **Invalidate stale receipts.** Any source, authority, fixture, generator, validator, dependency lock, runtime/compiler, workflow/Action revision, or comparison-option change invalidates prior promotion evidence unless the receipt schema explicitly proves it is outside the tested closure.

## Required canary receipt

Fleet tooling should consume a versioned, canonicalized, self-digesting receipt rather than infer success from badges. See [#44](https://github.com/ORESoftware/.github/issues/44).

A receipt must bind at least:

- production source repository and immutable candidate SHA;
- test organization/repository and immutable test head SHA;
- authored authority artifact digests and provenance;
- TJSV or equivalent admission tool revision when applicable;
- language, runtime, compiler/toolchain and package-manager identity;
- reviewed third-party GitHub Action commit SHAs used by required workflow steps;
- workflow run IDs and job IDs;
- explicit job step count and conclusion;
- required vs optional witness classification;
- zero-step/skipped/missing-evidence detection;
- source/test freshness relationship;
- normalized status: `passed`, `failed`, `partial`, or `stopped_for_evaluation`;
- digest of the complete receipt with deterministic canonical serialization.

`passed` is permitted only when all required witnesses executed and succeeded. No preferred authority or runtime may win by fallback.

## 2026-09-09 logging canary evidence

Candidate source heads used for the first slice:

- canonical: `ores-otel/ores.otel.log@20b296e817a04dfc4eb0515635ce036d8f4e984e`;
- legacy: `ORESoftware/next-loggers.ts@d49cc63a7073c538b368adabd0899289a948417a`.

### Green and merged test-org witnesses

- canonical Node;
- canonical Rust;
- canonical Go;
- canonical Dart;
- canonical Gleam;
- legacy Node.

### Deliberately red diagnostic witnesses

- legacy Rust: contract passes; native check finds rustfmt drift and a misspelled `ShutdownTriggger` type. Task: [next-loggers.ts#36](https://github.com/ORESoftware/next-loggers.ts/issues/36).
- legacy Go: contract passes; native compile/tests expose `Span.IsRecording`, shutdown API, and lint-fixture drift. Task: [next-loggers.ts#37](https://github.com/ORESoftware/next-loggers.ts/issues/37).
- legacy Dart: contract passes; analyzer/tests expose broad shutdown/logging/OTEL/Supabase/test-dependency drift. Task: [next-loggers.ts#38](https://github.com/ORESoftware/next-loggers.ts/issues/38).
- legacy Gleam: contract passes; native compile reaches removed `gleam/erlang/process.start`. Task: [next-loggers.ts#39](https://github.com/ORESoftware/next-loggers.ts/issues/39).

These failures are source defects or source/test semantic drift. They are not evidence that the peer-authority contract model should be weakened.

### Repair-wave checkpoint observed later on 2026-09-09

Source repair PR [next-loggers.ts#41](https://github.com/ORESoftware/next-loggers.ts/pull/41) was observed at `7389cda270dd44cba45e51050d756e810689c51e`. At that checkpoint `Context and shutdown contract`, `Server lifecycle audit`, and the r2g installed-consumer workflow were green, while `Observability hardening` run `34389154609` remained red across Rust, Go, Erlang/Elixir, TypeScript contract tests, Java, and Dart. Node package-export checks were green on Node 18/20/22/24 and remain a useful positive control.

The active downstream runs continued to show independent contract/native behavior: Rust exact-head run `34388788217`, Go `34374864141`, Dart `34374963823`, and Gleam `34375059759` all reached the shared contract witness before their native-runtime blocker. These are historical checkpoint identifiers, not permanent release pins; promotion must always use fresh exact-head evidence.

Rust also demonstrated why evidence text must be bound to the tested closure: its canary branch advanced to an intermediate source pin while its PR body still named an older source SHA. The machine-readable receipt and human-facing summary must agree with the actual tested source/test/tool heads.

## Follow-up task registry

- [next-loggers.ts#40](https://github.com/ORESoftware/next-loggers.ts/issues/40): add source-side polyglot native SDK CI so test-org canaries become an independent second witness instead of the first detector.
- [ores-otel-test/.github#3](https://github.com/ores-otel-test/.github/issues/3): extend canonical/legacy exact-head canaries to Python, Java, Ruby, Erlang, Elixir, WASM, and wire interop.
- [ores-otel-test/.github#4](https://github.com/ores-otel-test/.github/issues/4): replace mutable Action tags with reviewed full-SHA pins and remove Node-20-era action drift.
- [ORESoftware/.github#165](https://github.com/ORESoftware/.github/issues/165): add a pinned, fail-closed TJSV convergence gate to the next-loggers source/canary path instead of treating Python JSON Schema validation as equivalent convergence evidence.
- [ORESoftware/.github#77](https://github.com/ORESoftware/.github/issues/77): define the repository-local TJSV consumer lock and fail closed on executable/documentation pin drift.
- [shared-auth-test/.github#17](https://github.com/shared-auth-test/.github/issues/17): canary the latest reviewed TJSV revision across Shared Auth server/API/MCP and TypeScript/Rust/Go/Dart consumers before production pin advancement.

## TJSV promotion rule

A newer `ORESoftware/typespec-json-schema-validator` commit may be tested in `*-test` organizations without changing production consumers. Production pins remain on the last audited revision until the newer immutable candidate has passed the required test-org authority, Contract IR, differential-validation, language/runtime-boundary, and native consumer gates.

A TJSV canary must explicitly assert the checked-out 40-character validator revision. Generated JSON Schema remains a comparison witness; it never becomes a third editable authority.

The next-loggers audit exposed a concrete adoption gap: inspected exact-head canary paths currently run Python `jsonschema` plus source fixture checks, and repository search found no visible `typespec-json-schema-validator`/`tjsv` invocation in `ORESoftware/next-loggers.ts` or the inspected legacy Go canary. Python JSON Schema validation remains useful as an independent witness, but it is not peer-authority convergence proof. [#165](https://github.com/ORESoftware/.github/issues/165) owns that bounded adoption gap. If one independently authored authority lane is genuinely absent, record `stopped_for_evaluation`/architecture debt rather than synthesizing an authority from the other lane merely to make CI pass.

## GitHub Actions hardening

Canary workflows are evidence-producing supply-chain code. Follow account-level `agents.md`:

- pin third-party Actions to full reviewed commit SHAs;
- retain the readable upstream release/version in an adjacent comment where useful;
- select revisions whose declared runtime is supported by the current GitHub runner instead of relying on runner-side runtime coercion;
- set least-privilege workflow permissions;
- use explicit timeouts and concurrency cancellation;
- checkout with `persist-credentials: false`;
- do not expose privileged credentials to fork-originated runs;
- retain enough workflow/job metadata to distinguish real execution from zero-step or skipped jobs;
- bind required Action SHAs into the canary receipt so workflow supply-chain changes invalidate stale evidence.

The inspected legacy Go workflow uses mutable `actions/checkout@v4`, `actions/setup-python@v5`, and `actions/setup-go@v5`; the 2026-09-09 runner warned that Node-20-based Actions were being forced onto Node 24. Canonical task [ores-otel-test/.github#4](https://github.com/ores-otel-test/.github/issues/4) owns this repair. Runner or Action modernization must not suppress a source compatibility failure.

## Recommended execution order

1. Repair and recertify the bounded legacy Rust failure.
2. Repair and recertify Gleam process/context semantics.
3. Treat Go and Dart as larger semantic reconciliations with recent history and contract manifests, not mechanical test deletion.
4. Add source-side native CI in `next-loggers.ts`.
5. Add the next-loggers TJSV/admission gate and lock/receipt evidence without collapsing peer authorities.
6. Expand the remaining `ores-otel-test` languages.
7. Modernize/pin test-org Actions without hiding native failures.
8. Canary newer reviewed TJSV revisions in isolated test-org consumers before production pin advancement.
9. Implement the machine-readable receipt and make `oresc`/fleet automation fail closed on incomplete required canary sets.
