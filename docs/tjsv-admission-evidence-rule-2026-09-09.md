# TJSV admission-root and failure-evidence rule

Tracking: `DEN-3959`, `ORESoftware/.github#206`

This is the public-safe fleet rule discovered during bounded cross-runtime Lambda consumer rollout. Private repository assignments, authenticated run identifiers, and access details remain in Linear and approved private systems.

## Contract authority

For every contract crossing a language, runtime, process, or provider boundary:

- human-authored TypeSpec and human-authored JSON Schema Draft 2020-12/OpenAPI remain independent peer authorities;
- `ORESoftware/typespec-json-schema-validator` (TJSV) compares those authorities fail-closed at a reviewed immutable commit SHA;
- generated JSON Schema, Contract IR, generated clients, runtime serializers/deserializers, provider fixtures, and execution receipts are evidence only;
- a generated artifact must never become a third authored authority or silently replace either peer authority.

## Admission dependency rule

The TJSV contract job is a dependency root for any downstream check or promotion that assumes the cross-runtime contract has been admitted. As applicable, this includes:

- Rust/TypeScript/Dart/Go runtime witnesses;
- architecture checks;
- Docker/OCI builds;
- provider-adapter tests;
- package/publish jobs;
- deployment or promotion jobs.

A downstream green job does not override an unexplained TJSV mismatch. Jobs that rely on admitted contracts should normally express an explicit dependency on the contract job rather than racing independently.

## Failure taxonomy

Keep these states separate in receipts and status reporting:

1. `runner_admission_blocked` — no hosted step executes; this is not a TJSV or source-code verdict.
2. `contract_mismatch` — TJSV executes and finds structural or differential disagreement between the authored authorities.
3. `runtime_failure` — contract admission passed, but a native/runtime/provider witness fails.
4. `artifact_or_architecture_failure` — admitted source fails to build/package/run for an intended target.
5. `passed` — every required gate for the same candidate closure executed and passed.

Skipped, stale, missing, zero-step, or inaccessible evidence is not success.

## Preserve parity evidence on failure

TJSV report, SARIF, generated comparison output, and relevant receipts should remain inspectable even when TJSV exits nonzero.

When the evidence directory is dot-prefixed, a pinned `actions/upload-artifact` step must explicitly include hidden files, for example:

```yaml
- name: Retain TJSV parity evidence
  if: ${{ always() }}
  uses: actions/upload-artifact@<reviewed-full-sha>
  with:
    path: .typespec-json-schema-validator/
    include-hidden-files: true
    if-no-files-found: warn
```

An alternative is an intentionally non-hidden evidence directory. In either case, an empty/missing receipt must be reported as missing evidence, not a successful upload.

## Sealed-object regression

Object sealing semantics are contract semantics. TJSV must reject authored/generated disagreement such as `additionalProperties` versus `unevaluatedProperties` when those keywords produce different structural meaning under the selected Draft 2020-12 evaluation model.

Consumer authors should reconcile the two independently authored authorities based on intended wire behavior and the reviewed validator profile. They must not copy generated schema wholesale into the authored lane merely to turn the gate green.

Add regression coverage that proves:

- a deliberate sealed-object mismatch blocks promotion;
- the mismatch is classified as a contract failure rather than runtime failure;
- the failure receipt is retained;
- after semantic reconciliation, the same contract passes before downstream runtime/architecture jobs execute.

## Repository meta-policy

Repository-local verification should fail when any required contract-control surface disappears, including:

- the TypeSpec authority;
- the independently authored JSON Schema/OpenAPI authority;
- the immutable TJSV invocation;
- required evidence retention;
- downstream dependency on contract admission where applicable.

The purpose is to make removal of contract enforcement an explicit reviewed change rather than silent CI drift.

## Promotion rule

Promote only with authoritative remote evidence for the exact proposed candidate: pushed commit, PR, required TJSV receipt, applicable runtime/architecture/artifact/provider checks, and merge SHA after merge. Do not use transcript credentials, mutable refs, copied private source, or weakened checks to manufacture green evidence.
