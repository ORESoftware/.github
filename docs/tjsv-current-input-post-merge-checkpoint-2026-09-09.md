# TJSV current-input promotion post-merge checkpoint — 2026-09-09

Tracking: Linear `DEN-3830`; parent program `ORESoftware/.github#36`.

This is an append-only execution checkpoint. It updates the implementation state recorded earlier in `tjsv-source-revision-and-lambda-adversarial-checkpoint-2026-09-09.md`; it does not rewrite that historical snapshot or claim fleet rollout completion.

## Authority invariant

- Independently authored TypeSpec and independently authored JSON Schema/OpenAPI remain peer editable authorities.
- TypeSpec-generated Schema B, Contract IR, runtime evidence, package artifacts, Protobuf/WIT, generated clients, receipts, canaries, and fleet summaries remain evidence/projections only.
- No generated artifact may overwrite an authored authority or resolve a disagreement by fallback.
- Any unexplained, stale, incomplete, unsupported, wrong-revision, or wrong-artifact required evidence remains `STOPPED_FOR_EVALUATION`.

## Repaired Lambda merge lineage

`ORESoftware/typespec-json-schema-validator#84` merged the semantic reconciliation for the Lambda runtime-boundary fixture after stricter admission rules had advanced independently on `main`.

The repair preserved the hardened production verifier and updated the fixture/evidence witness to require:

- explicit empty parity findings;
- executed differential validation and positive probe counts;
- zero differential divergences/refusals;
- a complete nonempty Contract IR declaration inventory;
- explicit empty excluded/out-of-scope declaration inventories;
- exact parity-receipt and Contract-IR bindings for Rust/native, TypeScript/Node, and Dart/Flutter evidence.

This is the canonical repair lineage. Stale PR `#80` is retained only as provenance and must not be merged merely because it remains open.

## Release-package boundary — post-merge verified

`ORESoftware/typespec-json-schema-validator#87` salvaged the unique package-surface work from stale/red `#81` onto repaired current main without rewriting the historical branch.

Merged commit: `57fe9ba98555e7b02d9bb1481ed6b4bf427aaddc`.

The release preflight now verifies the packed, clean-consumer surface rather than trusting repository-local imports. It checks the public language-boundary verifier/type exports, all required Draft 2020-12 schema files, exact packed paths, package identity, lifecycle-script-blocked clean installation, public subpath import/resolution, and deterministic fail-closed empty-input behavior.

The merge commit passed Ubuntu 24.04 and macOS 14 post-merge CI in run `34393560041`.

Stale PR `#81` remains provenance only; its unique package work has been salvaged by `#87`.

## Current-input promotion boundary — post-merge verified

`ORESoftware/typespec-json-schema-validator#86` adds the preferred public promotion entrypoint:

`@oresoftware/typespec-json-schema-validator/language-boundary-current-inputs`

The implementation exposes `verifyLanguageBoundariesAgainstCurrentInputs()` and deliberately reuses canonical `verifyContractIr()` rather than creating another Contract-IR/parity verifier.

Before runtime evidence can be admitted, the wrapper requires explicit current paths for:

1. authored TypeSpec;
2. TypeSpec-generated Schema B;
3. independently authored Schema A.

It then freshly verifies the retained Contract IR against the retained parity receipt and those current inputs. The supplied, computed, and expected Contract-IR IDs plus retained parity `runId` must agree before the existing pure `verifyLanguageBoundaries()` policy is invoked.

Exact PR head: `fa6c3bd2084653f41c616b9c7397911020a25a61`.

Exact-head CI run `34393748659` passed Ubuntu 24.04 and macOS 14, including production-dependency policy, syntax/flags contract, unit and compiler-backed integration gates, package-boundary audit, and release preflight.

Merged commit: `e609e1973fcdcfaeecbdfa2dcbfde75c55286ff7`.

Post-merge CI run `34395786827` passed Ubuntu 24.04 and macOS 14. The implementation state is therefore `post_merge_verified`, not merely `implemented` or `merged`.

Integration coverage proves the preferred entrypoint fails closed for:

- stale independently authored Schema A bytes;
- a forged retained parity-report source digest;
- a tampered Contract-IR identity;
- runtime evidence bound to a different parity receipt;
- missing explicit current-input paths.

Filesystem/compiler/schema failures collapse to stable public-safe rules; source content, exception text, environment values, credentials, and private paths are not promoted into the public verification receipt.

## Current status corrections

The earlier checkpoint correctly recorded the state that existed when it was merged. This newer checkpoint records the subsequent transitions:

| Work | Earlier state | Current state |
| --- | --- | --- |
| TJSV #86 current-input promotion | red / not merge-ready | `post_merge_verified` at `e609e1973fcdcfaeecbdfa2dcbfde75c55286ff7` |
| TJSV #87 release-package preflight | review-blocked/open | `post_merge_verified` at `57fe9ba98555e7b02d9bb1481ed6b4bf427aaddc` |
| TJSV #80 stale fixture salvage | red/open | provenance only; canonical Lambda repair is #84 |
| TJSV #81 package preflight source branch | red/open | provenance only; unique work salvaged by #87 |

Do not close, reset, rebase, force-update, or merge the stale provenance branches solely to make the dashboard look clean. Preserve their history unless explicitly instructed otherwise.

## Next bounded implementation work

Duplicate/task-budget review found existing canonical owners, so this checkpoint refines those tasks instead of creating parallel issue clusters.

### P0 — public evidence grammar versus executable behavior

Owner: `ORESoftware/typespec-json-schema-validator#79`.

Now that current-input promotion is post-merge verified, make every public language-boundary Draft 2020-12 envelope and the executable verifier prove lockstep behavior. Schema-invalid envelopes must never be accepted by JavaScript, and every emitted verifier receipt must validate against its published receipt schema. Keep cross-object semantic rules explicit where JSON Schema is not the correct layer.

### P0 — cross-revision splice refusal

Owners: `ORESoftware/.github#131` and parent `#36`.

Construct one candidate evidence graph from individually valid artifacts produced by two different source revisions. Require admission to stop even when every component is independently well-formed. Extend revision coherence beyond witness-to-witness checks to retained parity/current-input evidence, Contract IR, consumer lock, runtime/package digests, and toolchain identity where the active profile requires it.

### P0 — merge-result/current-base proof

Owner: parent `ORESoftware/.github#36` and exact-head policy work.

Treat `exact_head_ci_passed`, `merge_tree_verified`, `merged`, and `post_merge_verified` as different states. A green branch head against an obsolete base is not sufficient evidence after relevant mainline semantic changes.

### P1 — reusable immutable consumer pin

Owners: `.github#37`, `.github#77`, `.github#55`.

Package the preferred current-input API into reusable CI and bind consumers to an exact reviewed validator revision. Upgrades must pass compatibility review and produce a reviewed pin-change PR; symbolic/latest references cannot become promotion evidence.

### P1 — bounded candidate rollout

Owner: `.github#168` plus the target `*-test` canary work.

Promote the newly verified validator revision through a bounded tranche rather than fleet-wide blind repinning. Require exact current source closure, consumer lock, runtime evidence, package-surface proof, and named-profile receipts for each canary.

### P2 — operational promotion and aggregation

Owners: `.github#57` and `.github#60`.

Only after the prerequisite evidence layers are current should package/release/deployment admission and fleet aggregation consume them. An aggregator reports evidence; it does not manufacture or strengthen a weaker receipt.

## Status vocabulary

Keep these states distinct in GitHub, Linear, canary receipts, release evidence, and dashboards:

- `planned`
- `implemented`
- `exact_head_ci_passed`
- `merge_tree_verified`
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
- `historical_pass`
- `stopped_for_evaluation`

This checkpoint advances #86 and #87 only through `post_merge_verified`. It does not claim canary or fleet completion.
