# DEN-3043 fleet data-registry admission and follow-up map — 2026-09-09

Status: active execution record  
Linear coordination: `DEN-3043`  
Implementation seed: `ORESoftware/k8s-libs-and-shared-defs#82`

## Current implementation evidence

`ORESoftware/k8s-libs-and-shared-defs#82` implements a queryable fleet metadata plane with 13 relations for contract identity/version/artifact/parity receipts, service and NATS bindings, database placement, external provider references, migration receipts, and database capability snapshots.

The implementation preserves these authority boundaries:

- independently authored TypeSpec and JSON Schema Draft 2020-12 are peer top-level authorities;
- generated TypeSpec JSON Schema is comparison evidence only;
- `table-map.json` is the explicit contract-model to SQL-relation projection;
- `nats/subject-defs` remains the NATS subject/queue/stream/fingerprint authority;
- product persistence authority remains with each product's parity-certified contract home rather than this registry.

Current exact PR head at the time of this record: `55ea67fecfecb8b1f3a69c7319a50af8a65e5104`.

Branch-matched verification recorded on that head:

- 16/16 Node relational/semantic tests pass;
- 17/17 checked-in positive/negative Draft 2020-12 corpus verdicts pass under an independent validator;
- 311/311 synthesized boundary checks pass across all 13 models, including missing-required, unknown-field, wrong-type, regex/pattern, and numeric-minimum cases;
- branch is 42 commits ahead and 0 behind `main`, with no deletions.

These are useful source-level/adversarial results, but they do not substitute for required exact-head hosted admission.

## Canonical TJSV admission shape

The consumer workflow pins exact validator revision:

`ORESoftware/typespec-json-schema-validator@4a5d049218adc2740d4cf78f612caf7f38f6f64c`

The gate requires:

1. independently authored TypeSpec plus Draft 2020-12 JSON Schema;
2. explicit declaration mapping for all 13 contract models;
3. positive and negative instance corpus;
4. 128 differential probes per declaration;
5. deterministic parity JSON receipt and SARIF;
6. digest-bound `ores.typespec-json-schema-validator.contract-ir/v1`;
7. positive receipt `status=passed`, zero unexplained findings, admissible Contract IR, exact receipt-run binding, and complete declaration scope;
8. a deliberate temporary one-lane drift canary that must stop evaluation and emit a non-admissible Contract IR tombstone.

Generated schemas, Contract IR, runtime projections, normalized catalogs, and receipts remain evidence. None becomes an independently editable schema authority.

## Hosted execution blocker

Current `fleet-data-registry-contract` run `34420666365`, job `102695141386`, was created for the exact PR head but executed zero steps. GitHub reports `runner_id=0`, an empty runner name/group, and no job log URL.

Per account/repository agent policy, this is `not_executed` / admission infrastructure failure. It is neither a passing test nor evidence that TJSV or the source contract failed. PR #82 must remain unmerged until the required exact-head steps actually execute.

Existing owner: [`ORESoftware/.github#52`](https://github.com/ORESoftware/.github/issues/52). A fresh #82 canary was appended there.

## Deduplicated follow-up ownership

| Workstream | Owner | Required result |
| --- | --- | --- |
| Reusable TJSV language/runtime admission | [`#37`](https://github.com/ORESoftware/.github/issues/37) | Package the exact-pin peer-authority + mapping + receipt + Contract IR + adversarial canary shape so consumers do not hand-roll divergent workflows. |
| Zero-step / runnerless exact-head admission | [`#52`](https://github.com/ORESoftware/.github/issues/52) | Restore trustworthy runner allocation and machine-readable `not_executed` vs `failed` vs `stopped_for_evaluation` vs `passed`. |
| Fleet registry immutable evidence identity | [`#191`](https://github.com/ORESoftware/.github/issues/191) | Bind registry claims to real parity/Contract-IR/runtime/current-input receipt identities rather than summary booleans. |
| Stale duplicated TJSV revision literals | [`#197`](https://github.com/ORESoftware/.github/issues/197) | Replace contradictory scattered validator literals with one explicit versioned provenance input per admission profile while retaining full immutable SHAs. |
| Live PostgreSQL/CockroachDB catalog conformance | [`#198`](https://github.com/ORESoftware/.github/issues/198) | Apply/introspect portable DDL on disposable engines, normalize live catalogs, exercise constraints, and bind results to migration/capability receipts. |

Runtime/language projection work belongs under #37 and the existing TJSV rollout program, not a duplicate DEN-3043 implementation. Real consumer languages must be discovered and executed; unsupported adapters must not be fabricated merely to satisfy a matrix.

## Immediate execution order

1. Fix/restore exact-head Actions runner execution under #52.
2. Execute #82's pinned positive and deliberate-negative TJSV/Contract-IR gate on the exact head.
3. Merge #82 only after applicable exact-head repository and contract checks have actually executed successfully.
4. Package the successful shape through #37 and eliminate stale policy pin drift through #197.
5. Bind retained evidence identities into the fleet registry through #191.
6. Add disposable live-catalog evidence through #198, keeping Neon/Supabase behavior as provider overlays over the portable PostgreSQL contract.

## Security and credential handling

Do not place PATs, Linear API keys, cloud credentials, DSNs, provider service-role keys, decrypted SOPS values, or other secrets in issues, pull requests, registry rows, fixtures, logs, receipts, or artifacts. Provider/resource fields carry identifiers or digests only. Credential mutation, revocation, or rotation is separate operational work and is never implied by this roadmap.
