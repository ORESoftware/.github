# Shared-interface admission and TJSV convergence

Tracking: DEN-3958, DEN-3959, DEN-3828, DEN-3830, DEN-390.

This document defines the ORESoftware organization-level policy for promoting shared interface contracts into reusable packages and downstream tools such as `ores-cli`.

It is intentionally an admission and evidence policy, not a new schema authority. Repository-local contract definitions and stricter repository policies remain authoritative for their own scope.

## 1. Authority model

For contract families that use the ORESoftware dual-authority model:

- TypeSpec is independently authored authority A.
- JSON Schema Draft 2020-12 is independently authored authority B.
- Neither authority is generated from the other and neither wins by fallback.
- TypeSpec-generated JSON Schema is comparison evidence only.
- Contract IR, SARIF, parity receipts, consumer-verification receipts, generated SDKs, runtime validators, Protobuf/WIT/SQL projections, and language-boundary receipts are derived evidence only.
- An unexplained structural or behavioral disagreement stops admission. Do not add an ignore mapping merely to make CI green.

`ORESoftware/typespec-json-schema-validator` (TJSV) is the canonical convergence and evidence tool for these peer authorities. Consumers must not create a second independent parity engine.

## 2. Repository roles

The normal layering is:

1. **Origin/source repository** — owns the independently authored contract files and any recorded corpus. Existing source contracts stay in place during shared-package rollout unless a separate reviewed migration explicitly authorizes extraction or removal.
2. **Shared interface package** — packages an admitted public/isomorphic subset while preserving immutable source provenance. It must not become a competing editable authority.
3. **Runtime/core libraries** — implement validation, construction, and runtime behavior. Shared interface repositories do not absorb runtime logic that belongs in `*-lib-core` / `*-pub-lib-core`.
4. **Clients/CLI/services** — consume admitted contracts and runtime libraries; they do not invent another schema ruleset.
5. **Independent test consumers** — verify package/runtime behavior without becoming production authority.

For the current ORESoftware shared-validation slice:

- compatibility/origin source: `ores-otel/ores-interfaces`;
- shared source package: `ORESoftware/ores-interfaces`;
- validator: `ORESoftware/typespec-json-schema-validator`;
- downstream standards consumer: `ORESoftware/ores-cli`.

## 3. Immutable source closure

A source package must declare the complete immutable closure required to reproduce admission. A source revision is not adequately pinned when auxiliary admission inputs are silently omitted.

The closure can include:

- TypeSpec source entry and transitively required source files;
- independently authored JSON Schema source;
- positive/negative instance corpus;
- mapping or declaration-scope policy where explicitly required;
- the source repository's TJSV `source-lock.json` or equivalent immutable validator policy;
- licenses/attribution needed to redistribute the public package.

Tests that reconstruct a packed/external consumer must reproduce this complete closure. If upstream admission adds a source-lock or another required source-owned policy file, consumers must carry that file rather than weakening upstream admission.

Source closure checks should be fail-closed and include, where applicable:

- exact 40-character Git revisions;
- exact checkout HEAD verification;
- clean tracked/index state;
- no symlink or redirected-Git-metadata substitution;
- no hidden tracked changes through skip-worktree/assume-unchanged/filter tricks;
- bounded reads and explicit source inventory;
- source unchanged before and after admission.

## 4. TJSV pin convergence

Validator version skew is a release-governance problem, not merely a dependency-update detail.

Source packages, shared packages, installers, and CI may advance on different pull requests, but promotion must have an explicit, machine-checkable verdict.

Until a reviewed release-channel manifest is implemented, the conservative rule is:

- the shared package must use the exact TJSV revision declared by its pinned source admission policy;
- downstream consumers must record the shared package's exact validator revision in provenance;
- a downstream tool that also distributes/installs TJSV must detect and report any different installed/distribution revision rather than silently assuming compatibility;
- exact equality may be required for a promotion gate when the consumer relies on validator-version-specific receipt semantics;
- a future compatibility window is allowed only when it is explicit, machine-readable, tested in both directions, and cannot silently admit an unknown future validator.

The durable follow-up is one reviewed release/channel record consumed by source packages, shared packages, installers, and CI. Superseded pins remain visible in Git history/evidence; do not rewrite old receipts.

## 5. Canonical package admission sequence

A shared interface package should follow this sequence:

1. Check out the exact reviewed package head.
2. Resolve the package's immutable source and TJSV revisions from checked-in policy.
3. Check out both dependencies at those exact revisions with `persist-credentials: false`.
4. Install TJSV from its committed lockfile.
5. Run source-policy/filesystem tests.
6. Execute real TJSV `check` over TypeSpec + independently authored JSON Schema plus the recorded corpus.
7. Require differential validation, direct declaration inventory, source-mutation checks, zero unexplained findings, and complete declared scope.
8. Produce Contract IR outside authored source directories.
9. Execute current-input `verify-ir` / consumer verification against the exact retained authorities and complete declaration inventory.
10. Build the package only while fresh admission evidence exists.
11. Exercise the actual packed package from another directory/process boundary.
12. Recompile/import the TypeSpec package and consume the JSON Schema/package exports through normal package resolution.
13. Re-run admission over packed source bytes and the complete source closure.
14. Require source/dependency checkouts to remain unchanged.
15. Retain evidence artifacts without treating retention as approval.

A failed or stopped TJSV run is evidence of a stopped admission, not a reason to change authority precedence.

## 6. Downstream `ores-cli` consumption

`ores-cli` must reuse its existing contract audit path rather than adding another public parser or comparator.

The downstream shared-interface gate should:

- pin an immutable merged `ORESoftware/ores-interfaces` revision;
- build/admit the shared package through that repository's own policy;
- run the real Rust `oresc audit contract` path against the admitted TypeSpec and authored JSON Schema bytes;
- require the canonical TJSV parity report, Contract IR, and fresh consumer-verification receipt;
- bind the evidence back to the shared package manifest/provenance and complete declaration scope;
- validate any `ores-cli` TJSV distribution/source lock against the pin-convergence policy;
- keep `.cli-flags.toml` and official flags-2-env integration as the only public CLI flag/command authority.

A private GitHub Actions job that finishes with no runner steps (`steps: null`, `runner_id: 0`, or equivalent) is infrastructure admission evidence only. It is neither a source failure nor passing test evidence.

## 7. Language/runtime promotion

Source parity does not prove generated language/runtime parity.

For required generated/runtime targets, use TJSV language-boundary evidence (or the current canonical equivalent) after source admission.

Each required target should bind at least:

- canonical language/runtime identity;
- immutable source revision;
- artifact digest;
- exact parity `runId`;
- exact Contract IR `irId`;
- generator/toolchain name and version;
- passed ingress validation;
- passed egress validation.

Primary ORESoftware runtime targets are Rust, TypeScript/Node.js, Dart/Flutter, Gleam/BEAM, and Go. Expansion to 15+ languages should follow only after the primary targets have real evidence or explicit unsupported/refused results.

Optional targets may be absent. If optional evidence is supplied, it is validated with the same strict envelope; optional must not mean unchecked.

## 8. Zed publication and dependency installation

Do not fabricate `.zpkg.lock` entries or claim registry-backed installation from a metadata-only dependency declaration.

Before replacing source/tarball consumption with Zed:

1. shared-package admission and packed-consumer tests pass;
2. a reviewed immutable package is genuinely published/resolvable;
3. an external clean consumer runs real `zed install`;
4. only resolver-produced lock data is committed;
5. `zed install --frozen` succeeds in a clean consumer;
6. package identity/provenance remains bound to the admitted source/TJSV policy.

## 9. Independent consumer CI

Private repository CI can fail before runner execution. Independent test repositories are useful for separating toolchain/contract breakage from private-runner admission failures, but they must not leak private source.

A public/test-org consumer may contain:

- public contract fixtures;
- published/public package inputs;
- minimal consumer code using public APIs;
- immutable public toolchain pins;
- generated evidence that contains no private source or credentials.

A public test consumer passing does **not** automatically certify a private complete application tree. Private exact-head application tests remain required when runners execute.

## 10. Fleet migration

Shared-package rollout is additive by default.

For each consumer organization/repository, record:

- current origin/source authority revision;
- shared package revision, if adopted;
- TJSV revision/channel;
- runtime/projection revisions;
- admission/evidence status;
- whether legacy direct source consumption remains required;
- blockers and migration owner.

Do not delete original authority files merely because a shared package exists. Removal/extraction requires independent evidence that all required consumers, migrations, attribution, resolver identity, runtime validation, and rollback paths are satisfied.

## 11. Conflict-resolution policy

Shared-interface work frequently collides with fast-moving source/validator branches. Apply the organization semantic-conflict policy:

- inspect merge base and both heads;
- inspect surrounding commits, tests, contracts, and linked Linear work;
- preserve compatible intent from both sides;
- do not choose `ours` or `theirs` wholesale;
- prefer normal merge commits over rebase;
- preserve unique stale-PR tests/hardening with provenance rather than discarding them;
- validate the exact proposed head before merging.

## 12. Current rollout checkpoint (2026-09-09)

- `ORESoftware/ores-interfaces#2`: semantically reconciled and merged; unique raw JSON exponent-number regression retained after exact-head Ubuntu/macOS admission passed.
- `ORESoftware/ores-interfaces#6`: merged at `63802209da9e08ab54fec1c34a69cc0d58607377` after Ubuntu 24.04 and macOS 14 passed the complete source-lock closure, package-consumer, fresh package, and unchanged-checkout gates; Linux also passed Zed validation/task execution.
- `ORESoftware/ores-cli#40`: downstream immutable shared-interface consumer, now pinned to merged shared package `63802209da9e08ab54fec1c34a69cc0d58607377`; keep draft until its exact-head consumer/application evidence executes rather than ending as a zero-step private Actions job.
- `ORESoftware/ores-cli#42`: independently advances the installed TJSV revision beyond the current shared-package checkpoint, demonstrating why the pin-convergence/channel policy above is required before independent pin updates are treated as automatically compatible.

The current Linear project is `github.com/ORESoftware`; the project document `Shared interface admission + TJSV convergence follow-through` carries the issue-ready follow-up queue while new Linear issue creation is quota-blocked. Broad related tracking includes DEN-3958, DEN-3959, DEN-3828, DEN-3830, DEN-390, DEN-637, DEN-2050, DEN-2843, and DEN-3043.
