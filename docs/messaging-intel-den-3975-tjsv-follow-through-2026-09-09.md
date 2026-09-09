# Messaging Intel DEN-3975 TJSV QA/research boundary follow-through

Tracking: Linear `DEN-3975`; Messaging Intel project `github.com/messaging-intel`.

Last reconciled: 2026-09-09.

## Purpose

The original DEN-3975 documentation/product-boundary scope is complete, but the next implementation phase still needs executable exact-head evidence. This record turns those remaining gaps into bounded repository-owned tasks without reopening completed research-product scope or duplicating the account-level TJSV backlog.

Linear currently rejects new issue creation because the workspace is at its issue-row limit. The executable child tasks therefore live as GitHub issues and are mirrored in the Linear project document **DEN-3975 TJSV QA/research boundary follow-through — 2026-09-09**.

## Current evidence-backed blocker

`messaging-intel/msgint-interfaces#61` remains open/draft at head `4b4138e5acc6a29b9d287413e454d2ff93f3bae5`.

The exact-head workflow run `34315550474` exists for the dedicated `DEN-3975 workplace boundary TJSV and runtimes` workflow, but job `102350883785` received no runner (`runner_id=0`) and executed zero steps (`steps=[]`). This is a pre-admission execution-evidence failure, not a source-test failure.

Do not weaken tests, make private dependencies public, infer billing from `runner_id=0`, or merge using older-head evidence.

## New bounded tasks

### 1. Restore executable exact-head CI

`messaging-intel/msgint-interfaces#62`

Required outcomes:

- resolve the exact current PR head and mandatory workflow set immediately before merge decisions;
- classify missing-run, zero-step/pre-admission, credential-boundary, and executed-code failure separately;
- use existing bounded exact-head scheduling/dispatch infrastructure rather than inventing another dispatcher;
- require real-step execution for the dedicated TJSV/runtime lane and every mandatory repository gate;
- preserve independent TypeSpec and authored JSON Schema Draft 2020-12 peer authority;
- preserve no-recruitment, no-participation-status, no-manager-signal, and no-cross-system-identifier research/QA invariants.

Related account ownership: `.github#94`; Linear DEN-3440, DEN-3903, DEN-3982.

### 2. Bind current-input TJSV evidence through native consumers

`messaging-intel/msgint-interfaces#63`

Required evidence chain:

```text
authored TypeSpec
+ authored Draft 2020-12 JSON Schema
-> parity receipt
-> verified Contract IR
-> generated projection digest
-> native runtime execution
-> admitted runtime receipt
-> consumer evidence
```

The chain must bind exact source closure, validator revision, declaration inventory, comparison witness, parity receipt, Contract IR, corpus, adapter identity, generated projection digests and source commit. TypeScript/Node, Rust/Serde and Dart/Flutter must execute the same synthetic corpus.

Compare normalized accepted output and stable error/rule evidence, not verdict booleans only. Reject stale or forged receipts, changed current authorities, changed projections/corpus, missing mandatory evidence and declaration-inventory drift.

Public receipts may contain bounded verification metadata only. They must not contain participant or QA identity, reproductive/health observations, manager/team information, location/BLE/device data, telemetry linkage, raw fixtures, credentials or secret-bearing environment/argv data.

Dependencies: `ORESoftware/typespec-json-schema-validator#78/#79`; account `.github#65/#68/#43/#80`; Linear DEN-3830, DEN-3828, DEN-3959 and DEN-3982.

### 3. Add an independent test-organization canary

`messaging-intel-test/.github#12`

After the producer has executable exact-head admission, the test organization must independently consume an immutable producer commit and reviewed immutable TJSV revision, reverify source/provenance closure, run synthetic negative controls and emit a bounded canary receipt.

The canary must reject wrong source SHA, wrong Contract IR/projection/corpus digests, stale or expired evidence, zero-step CI, missing mandatory runtime cells and mandatory unsupported cells represented as pass.

No real participant, QA-worker, health/reproductive, manager/team, location/device or telemetry data may be used. The canary must not activate recruitment, consent, collection, compensation or production research endpoints.

Related ownership: Linear DEN-3425; account `.github#41/#44/#99/#101`.

## Critical path

1. `msgint-interfaces#62` — restore executable exact-head CI.
2. Validator prerequisites `typespec-json-schema-validator#78/#79` — current-input re-verification and public evidence-schema/executable conformance.
3. `msgint-interfaces#63` — complete the producer evidence lineage and native runtime proof.
4. `messaging-intel-test/.github#12` — independent immutable test-org canary.
5. Feed exact canary evidence into the existing fleet/release lanes only after those steps pass: DEN-3425, DEN-3982, DEN-3830 and account `.github#41/#44/#57/#60`.

## Existing work reused rather than duplicated

- DEN-3975 — semantic parent for the QA/research boundary; completed original scope stays completed.
- DEN-3903 — Messaging Intel CI admission and fleet verification.
- DEN-3440 — zero-step/runnerless Actions classification.
- DEN-3425 — Messaging Intel test-org fail-closed nightly evidence.
- DEN-3982 — recurring fleet cross-check and receipt lineage.
- DEN-3830 / DEN-3828 / DEN-3959 — cross-language contract compiler, downstream projections and dual-authority TJSV convergence.
- `ORESoftware/.github#36` — account-level TJSV rollout program.
- `ORESoftware/.github#94` — exact-head workflow scheduling after API/App-authored writes.
- `ORESoftware/.github#65/#68` — native-runtime semantic evidence.
- `ORESoftware/.github#99/#101` — evidence freshness/retention and public-safe redaction.

This follow-through does not create another contract authority, parity engine, dispatcher, participant identity bridge or research activation path.

## Stop conditions

Stop and evaluate if any required job is missing, skipped, zero-step, runner-blocked, stale, wrong-head, wrong-validator, wrong-profile, wrong-artifact, unsupported-but-green, or if public evidence contains private/research-participation/QA identity material.

Generated files, workflow YAML, previous-head CI, a passed-looking receipt object or a documentation checkbox never satisfy executable evidence by themselves.

## Completion standard

This phase is complete only when:

- the exact current producer head executes every required gate with real steps;
- the TJSV current-input/provenance chain is non-vacuous and adversarially tested across the named native runtimes;
- the independent test organization certifies an immutable producer revision;
- exact run/job/commit evidence is linked back to Linear and the owning GitHub issues; and
- no research/QA separation invariant is weakened.