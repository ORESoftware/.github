# TJSV second-wave task graph — 2026-09-09

Tracking: Linear `DEN-3830`; GitHub parent [`ORESoftware/.github#36`](https://github.com/ORESoftware/.github/issues/36).

This document records the next bounded task wave discovered after reconciling the current TJSV language/runtime-boundary roadmap, the Linear work breakdown, and the active GitHub issue graph. It supplements, rather than replaces, `docs/tjsv-language-boundary-rollout.md` and the execution-wave documents.

## Authority invariant

- Human-authored TypeSpec and human-authored JSON Schema/OpenAPI remain independent peer top-level authorities.
- `ORESoftware/typespec-json-schema-validator` (TJSV) is the required convergence/admission implementation for applicable cross-language/runtime contract evidence.
- Generated Schema B, Contract IR, runtime observations, compatibility receipts, version-policy receipts, dependency-cohort receipts, Protobuf/WIT, generated clients, build outputs, and fleet summaries are evidence/projections only.
- No generated artifact or historical version wins an unexplained disagreement by fallback.
- Missing, stale, unsupported, zero-step, nondeterministic, compositionally inconsistent, or profile-incomplete required evidence cannot be promoted as `passed`.

## Duplicate review and correction

The first compatibility proposal overlapped the already-existing [`#85`](https://github.com/ORESoftware/.github/issues/85), which is the canonical owner for backward/forward contract-evolution admission profiles and cross-version producer/consumer evidence.

Rather than leave a duplicate compatibility engine, [`#135`](https://github.com/ORESoftware/.github/issues/135) was narrowed to the downstream version-policy layer. It consumes an exact #85 compatibility receipt and decides whether a requested package/API/protocol version transition is allowed. #85 remains the temporal compatibility owner.

## New executable tasks

### #139 — repeat-run determinism admission

[`ORESoftware/.github#139`](https://github.com/ORESoftware/.github/issues/139)

A single exact-head green execution does not prove that TJSV admission itself is deterministic. This task requires multiple isolated executions over the same immutable source/toolchain/dependency closure, compares the canonical outputs that the selected assurance profile requires to be stable, and quarantines unexpected divergence.

The task is intentionally distinct from:

- #40, which owns reproducible build/executable provenance;
- #63, which owns mutation/fuzz/vacuity resistance; and
- #46, which owns qualified OS/architecture/WASM target evidence.

Expected evidence includes a versioned determinism receipt binding run identities, exact input closure, toolchain/platform identities, canonical output digests, allowed volatile-field policy, and bounded divergence fingerprints. Retrying until a flaky run happens to become green is not an acceptable promotion strategy.

Linear context: `DEN-3830`, `DEN-3828`, `DEN-3982`.

### #135 — semantic compatibility -> version-policy admission

[`ORESoftware/.github#135`](https://github.com/ORESoftware/.github/issues/135)

This task consumes the cross-version compatibility evidence produced by #85 and turns it into deterministic package/API/protocol version-policy decisions. It must not duplicate the compatibility comparator.

The policy should:

- map admitted compatibility classes and required producer/consumer directions to allowed patch/minor/major or profile-specific version transitions;
- refuse a nominal patch/minor claim when #85 proves a breaking or migration-requiring change;
- avoid treating a major version as permission for unexplained mismatches;
- emit a content-addressed version-policy receipt; and
- feed release gating plus dependency-risk automation rather than silently editing manifests or tags.

Linear context: `DEN-3433`, `DEN-3959`, `DEN-3828`; related dependency policy `DEN-3449`.

### #136 — exact multi-repository dependency-cohort admission

[`ORESoftware/.github#136`](https://github.com/ORESoftware/.github/issues/136)

Repository-local green receipts can still compose into an invalid polyrepo release. This task defines an immutable cohort manifest and receipt over the **resolver-produced** dependency graph so interfaces, lib-core, generated clients, servers, packages, and deployable artifacts cannot silently mix incompatible generations.

The cohort gate should:

- bind repository commits/tags, package/artifact digests, lock/graph digests, assurance profiles, and exact component receipts;
- reject symbolic refs, floating ranges, stale locks, wrong-artifact receipts, and transitive resolution drift;
- consume #85/#135 evidence for explicitly supported mixed-version cohorts;
- distinguish a staged rollout from a fully admitted cohort; and
- feed #57 release gates and #60 fleet aggregation without creating a second parity engine.

Linear context: `DEN-3798`, `DEN-3433`, `DEN-3449`, `DEN-637`.

## Dependency graph

Recommended order:

1. Stabilize TJSV's public/current-input evidence semantics: `typespec-json-schema-validator#79`, then `#78`.
2. Complete non-vacuity/mutation controls and named assurance vocabulary: `.github#63`, then `.github#54` where ordering constraints require the stable semantics.
3. Require repeat-run determinism for release-grade profiles: `.github#139`.
4. Package canonical reusable current-input admission and native runtime evidence: `.github#37`, plus the relevant runtime/platform tasks.
5. Produce explicit cross-version compatibility evidence: `.github#85`.
6. Derive version-policy admission from that evidence: `.github#135`.
7. Compose exact repository/package/artifact identities into a resolver-backed cohort receipt: `.github#136`.
8. Feed current #135/#136/#139 evidence into `.github#57` release/deploy gates, `.github#60` fleet ledger, `.github#55` upgrade automation, and the existing Linear dependency-risk programs.

## Stop conditions added by this wave

In addition to the existing roadmap stop conditions, promotion must stop when:

- repeated admission over the same declared closure produces unexplained canonical-output divergence;
- a requested package/API/protocol version transition contradicts the admitted compatibility evidence;
- a dependency resolver produces a component identity different from the one bound into the candidate cohort;
- individually valid repository receipts cannot be assembled into one compatible exact cohort; or
- a mixed-version rollout lacks the explicit compatibility directions and rollback boundary required by its selected profile.

## Linear synchronization

The canonical Linear project document is **TJSV language-boundary rollout work breakdown — DEN-3830 — 2026-09-09**. The same second-wave task graph has been appended there. Because the Linear workspace currently rejects new child issue creation at its issue-count limit, the executable bounded tasks live as GitHub issues while existing DEN issues remain their broader ownership contexts.

The GitHub parent issue #36 is also updated with this second-wave dependency graph. Documentation/roadmap completion must never be mistaken for implementation, exact-head CI, merge, canary, release, or fleet-rollout completion.
