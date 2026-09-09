# Exact-head CI and PR evidence backlog — 2026-09-09

Tracking controller: Linear `DEN-268`.

New durable GitHub tasks discovered in this pass:

- [`ORESoftware/.github#94`](https://github.com/ORESoftware/.github/issues/94) — guarantee exact-head Actions after GitHub App/API branch writes.
- [`ORESoftware/.github#98`](https://github.com/ORESoftware/.github/issues/98) — detect stale pull-request narratives after head/dependency drift.

A dedicated Linear issue was attempted for #94 on 2026-09-09, but Linear rejected creation because the workspace has reached its free issue limit. Until issue capacity is restored, these GitHub issues are the canonical task records and existing Linear controllers carry links/evidence. Do not invent DEN identifiers.

## Non-negotiable evidence rules

1. Merge, publish, release, and deployment evidence must belong to the **exact current pull-request head** and the required current base/policy context.
2. A successful run from an older head is stale evidence and cannot satisfy the current gate.
3. `no run exists`, `run exists but no step executed`, `code executed and failed`, and `credential boundary prevented execution` are separate states. Never collapse them into a generic red CI state.
4. `runner_id = 0` or zero steps alone is not evidence of billing. Billing requires an explicit GitHub billing/spending annotation or other authorized evidence.
5. A missing required exact-head run fails closed. Do not merge because previous-head CI was green.
6. Do not weaken workflows, remove contract gates, expose credentials, make private dependencies public, or substitute local/mock dependencies merely to turn a gate green.
7. TypeSpec and independently human-authored JSON Schema/OpenAPI remain co-equal authorities. TJSV is an admission/convergence gate and generated artifacts are evidence, not a third authority.

## Live canaries and current classification

| Repository / PR | Exact head | Observed state | Classification | Owner / next action |
| --- | --- | --- | --- | --- |
| `fiducia-cloud/fiducia-clients#105` | `4bbe327fcc397a3227b7ee8d1b977681fbffccc9` | PR-triggered Actions query returned zero runs for this SHA after the API-authored repair commit | `missing_exact_head_run` | `.github#94`; DEN-860 / DEN-3982. Schedule/dispatch bounded exact-head CI before any merge decision. |
| `ORESoftware/ores-cli#39` | `4f29ca7ac1be8c5e5c00973ed49d125fc2647daa` | CI run `34376564819`, attempt 3, job `102562751140`; `steps=[]`, `runner_id=0` | `pre_admission_zero_step` | DEN-3440 / DEN-2776. Keep unmerged; classify with machine evidence and rerun only through approved bounded paths. |
| `ORESoftware/ores-cli#40` | `a6773cec80096c0103f5630fee01273995f0bbbc` | PR body says shared-interface lock still needs advancing, but head already pins merged `ores-interfaces#2` commit `ace35ff7f85a4e1c78e4e71c9039a0f531c4cb82` | `stale_pr_narrative` | `.github#98`; DEN-3435 / DEN-3776 / DEN-3918. Reconcile managed status without deleting history or auto-promoting draft state. |
| `fiducia-cloud/fiducia-lib-core#6` | exact PR head tracked by owning PR | TJSV/Contract-IR gates execute; native Rust validation cannot read a pinned private cross-org dependency because the Actions credential is absent | `credential_boundary` | Existing `fiducia-cloud/fiducia-lib-core#7`; do not duplicate or weaken dependency/security boundaries. |
| `cliptown/cliptown-interfaces#30` | merged | deterministic generated outputs were stale; regenerated outputs then all eight exact-head workflows passed | `resolved_deterministic_artifact_drift` | Merged as `01a4e9f4838bd0d362ee8b68c641c9362d83ac4c`; preserve as a regression canary. |
| `ORESoftware/typespec-json-schema-validator#76` | merged | new regression test incorrectly expected no Contract IR on drift; production correctly emits a non-admissible tombstone | `resolved_test_semantics` | Merged as `4740f1367a7906813dcd420a77d0c9ede26943fb`; preserve tombstone fail-closed semantics. |

## Failure-state taxonomy

### `missing_exact_head_run`

No required Actions run is attached to the exact current head. This is a scheduling/event/dispatch evidence gap, not an executed test failure.

Required response:

- resolve current PR head SHA after the write;
- enumerate the repository's required workflow set;
- check for runs bound to that exact SHA;
- use the existing allowlisted least-privilege bounded dispatcher when normal synchronization did not schedule the workflow;
- emit an idempotent receipt keyed by repository + PR + workflow + head SHA;
- leave merge/publish/promotion blocked until exact-head evidence exists.

Canonical task: `.github#94`.

### `pre_admission_zero_step`

A workflow/job record exists, but the job received no runner or executed zero steps. This is distinct from a missing run and from code failure.

Required response:

- feed the job/run evidence to the DEN-3440 classifier;
- preserve `unknown` unless explicit evidence proves a more specific cause;
- never infer billing from `runner_id=0` alone;
- avoid fallback for policy/ruleset/canceled/unknown states unless the classifier explicitly permits it.

Canonical Linear owner: `DEN-3440`; fleet reconciliation: `DEN-2776`.

### `executed_code_failure`

At least one relevant step actually ran and failed. Diagnose from the exact job logs; repair the code/configuration/derived artifact rather than reclassifying it as infrastructure.

### `credential_boundary`

A runner executes but cannot access an intentionally private dependency or service because the approved credential path is missing/incorrect.

Required response:

- use least-privilege GitHub App/secret-manager paths;
- do not make private repositories public;
- do not replace pinned upstreams with local mocks;
- keep immutable revisions and full verification enabled.

### `deterministic_artifact_drift`

Authoritative source or reviewed implementation changed while committed generated/manifest evidence did not.

Required response:

- regenerate from the authoritative source/generator;
- review the deterministic diff;
- commit the refreshed artifacts/receipts;
- rerun exact-head CI;
- never hand-edit hashes when a deterministic generator or workflow artifact is available.

Current Fiducia ownership: `DEN-860`, `DEN-3982`, and the owning contract issue.

### `stale_pr_narrative`

The PR description contains a live assertion about current code/dependencies/readiness that is no longer true for the current head.

Required response:

- compare machine-checkable claims against the current head tree, base, upstream merge state, and linked Linear/GitHub evidence;
- preserve human-authored history;
- update a bounded machine-managed status section or idempotent comment rather than silently rewriting arbitrary prose;
- do not auto-promote a draft or merge solely because a prose prerequisite now appears satisfied.

Canonical task: `.github#98`.

### `stale_evidence`

The evidence itself was once valid but its subject/policy revision moved. Existing evidence-admissibility rules in `DEN-3435` apply; recertify rather than rebinding old proof to the new subject.

## Linear ownership map

Use existing Linear work rather than creating duplicate tickets:

- `DEN-268` — cross-portfolio execution controller and temporary Linear-side index for #94/#98 while workspace issue creation is blocked.
- `DEN-3440` — fail-closed classification of zero-step / runnerless Actions admission failures.
- `DEN-2776` — residual GitHub Actions admission and branch-protection reconciliation.
- `DEN-3435` — stale evidence invalidation and recertification.
- `DEN-3779` — bounded exact-head Actions dispatch/offload mechanism; extend/reuse, do not create another dispatcher.
- `DEN-3426` — reusable workflow-governance/exact-head policy.
- `DEN-3776` — exact-head PR reviewer; natural integration point for PR-narrative assertions.
- `DEN-3918` — fleet PR readiness/recovery queue.
- `DEN-860` — Fiducia client generator/conformance and deterministic drift.
- `DEN-3958` — shared interfaces consumed across client SDK languages / `ores-cli` integration lineage.
- `DEN-3982` — fleet TypeSpec/JSON Schema cross-check and receipt lineage.
- `DEN-3959` — independent TypeSpec and JSON Schema/OpenAPI authority/convergence policy.

## Immediate execution queue

1. **Implement #94 canary path** using `fiducia-clients#105`: exact-head write detection -> required-workflow resolution -> bounded idempotent scheduling/dispatch -> receipt.
2. **Keep `ores-cli#39` blocked** until a job executes real steps for head `4f29ca7...`; add this canary to DEN-3440 without relabeling it billing.
3. **Keep `ores-cli#40` draft** until its exact-head workflows execute. Separately reconcile its stale PR narrative through #98; the already-correct `ace35ff...` source lock is not itself a blocker.
4. **Finish `fiducia-clients#105` only after fresh head CI exists**. If canonical client-API manifest drift remains, regenerate from deterministic evidence and rerun all required lanes before merge.
5. **Do not duplicate `fiducia-lib-core` private dependency auth work**: continue through existing GitHub issue `fiducia-cloud/fiducia-lib-core#7` and its existing Linear credential-plane ownership.
6. **Extend the fleet scanner** to count these states separately so dashboards/merge automation never report `missing`, `pre_admission_zero_step`, or `credential_boundary` as ordinary test failures.
7. **Add PR assertion drift detection** from #98 to the exact-head reviewer and use `ores-cli#40` as the first regression fixture.

## Completion standard

This backlog is not complete because an issue or document exists. Completion requires exact-head implementation and tests in the owning repositories, durable receipts, linked Linear/GitHub evidence, and merge only after the current head is independently verified. Infrastructure or credential blockers remain blockers; they are not permission to bypass the gate.
