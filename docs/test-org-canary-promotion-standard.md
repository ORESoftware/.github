# Test-org exact-head canary promotion standard

Status: account-level promotion standard under DEN-3959.

This document semantically salvages the still-useful policy from stale PR #62 onto current `main`. It preserves the original branch as provenance and incorporates the newer middleware canary evidence observed on 2026-09-11.

## Purpose

Sibling `*-test` GitHub organizations are isolated downstream witnesses for changes that cross repository, contract, language, runtime, package, or deployment boundaries. They are not generated mirrors and they are not permission to weaken production gates. Their job is to prove that one immutable candidate source/tool revision is consumable by an independent downstream harness before promotion.

A test-org pass supplements source-repository CI; it never replaces a required source gate. A source-repository pass likewise does not replace downstream consumer execution.

## Required lifecycle

1. **Select immutable candidates.** Record the production repository plus a 40-character commit SHA and every validator, generator, contract, dependency-lock and workflow revision that affects admission. Mutable branches and tags are not evidence identities.
2. **Preserve peer authorities.** TypeSpec and independently authored JSON Schema/OpenAPI remain peer editable authorities. Generated Schema B, Contract IR, generated clients/types, protobuf/WIT, SQL and receipts are evidence/projections only.
3. **Bind the canary.** Check in the exact production and tool revisions under test. The test repository head becomes part of the evidence closure once CI begins.
4. **Separate contract and runtime witnesses.** TJSV convergence, native compilation, runtime behavior, transport behavior, packaging, reproducibility and deployment/container checks are separate witnesses. Passing one does not imply another.
5. **Treat non-execution as non-success.** Missing, queued, skipped, canceled, zero-step, runnerless, startup-failed, stale or otherwise non-executed required jobs are not green evidence.
6. **Keep diagnostic failures visible.** Do not delete a failing canary, weaken assertions, turn a required job optional, replace an immutable SHA with a mutable ref, or rewrite the consumer solely to manufacture green status.
7. **Repair the authoritative source.** When a canary exposes source drift, publish a focused source repair PR. Repoint the existing canary to that exact repair commit and rerun the same gates.
8. **Promote only one exact closure.** Required canaries must be green against the same exact source/tool/authority closure. Mixed evidence from different commits is `stopped_for_evaluation`.
9. **Requalify merge commits.** After production merges, repoint required canaries to the exact merged `main` SHA. A PR-head receipt is not automatically evidence for a distinct merge commit.
10. **Invalidate stale receipts.** Any relevant source, authority, fixture, generator, validator, dependency lock, toolchain, workflow/Action revision or comparison-option change invalidates earlier promotion evidence unless the receipt proves that input is outside its tested closure.

## Required canary receipt

Fleet tooling should consume a versioned, canonicalized, self-digesting receipt rather than infer promotion state from badges or PR prose.

A receipt must bind at least:

- production source repository and immutable candidate SHA;
- test organization/repository and immutable test head SHA;
- authored authority identities and content digests;
- TJSV revision and comparison options when contract admission applies;
- Contract IR/parity receipt identities when produced;
- language, runtime, compiler/toolchain and package-manager identities;
- dependency-lock digest or explicit lock-drift state;
- reviewed third-party GitHub Action commit SHAs;
- workflow run IDs and job IDs;
- actual step count plus job conclusion;
- required/optional witness classification;
- skipped, zero-step, startup-failure and missing-evidence detection;
- source/test freshness relationship;
- normalized status: `passed`, `failed`, `partial`, or `stopped_for_evaluation`;
- deterministic digest of the complete receipt.

`passed` is permitted only when every required witness executed and succeeded. No authority, validator or runtime wins by fallback.

## Diagnostic canaries are source-quality sensors

A canary can be behaviorally healthy and still be correctly red. Reproducibility, source formatting, lockfile consistency, source immutability and evidence binding are first-class promotion properties.

The 2026-09-11 ORES middleware wave is the current example:

- the Rust test-org canary compiled all feature projections, passed warning-denied Clippy, repeated portable/default/all-feature tests, passed an optimized all-feature test, validated the runtime descriptor and proved source immutability on Ubuntu and macOS; its final gate still failed because Rust 1.95 reported tracked-source rustfmt drift;
- the Gleam/OTP canary passed formatting/native tests, runtime descriptor validation, randomized adversarial execution and authored-source immutability, then failed the final dependency-metadata reproducibility gate;
- the Erlang/Cowboy canary passed compilation, repeated native tests, runtime descriptor validation, randomized adversarial execution and source immutability, then failed the dependency-lock reproducibility gate;
- the Elixir/Plug canary passed repeated native tests but exposed a runtime-descriptor contract failure in addition to formatting and lock reproducibility findings, so downstream adversarial promotion correctly did not run.

These are not reasons to weaken the canaries. They are actionable evidence directing repairs to the authoritative source or reproducible dependency metadata.

## TJSV promotion rule

A newer `ORESoftware/typespec-json-schema-validator` revision may be exercised in `*-test` organizations without immediately advancing every production consumer.

For TJSV-backed contracts:

- TypeSpec and authored JSON Schema/OpenAPI remain independent peer authorities;
- the canary must assert the exact 40-character validator revision;
- generated Schema B and Contract IR remain evidence only;
- structural findings cannot be erased merely because the differential corpus agrees;
- zero paired declarations is not evidence of semantic equivalence;
- positive admission should be paired with deliberate drift/negative controls where the contract risk warrants it;
- external-consumer/package-layout checks are distinct from source-checkout tests and should cover the supported OS/runtime matrix;
- production pin advancement waits for the reviewed candidate to pass the required authority, current-input, differential, language/runtime-boundary and consumer gates.

If one independently authored authority lane is genuinely absent, record architecture debt or `stopped_for_evaluation`; do not synthesize one authority from the other merely to make CI pass.

## GitHub Actions hardening

Canary workflows are evidence-producing supply-chain code. They should:

- pin third-party Actions to reviewed full commit SHAs;
- use least-privilege permissions;
- use explicit timeouts and concurrency cancellation;
- checkout exact heads with `persist-credentials: false`;
- avoid privileged credentials on fork-originated runs;
- retain enough workflow/job metadata to distinguish execution from runner/admission failure;
- prove checked-out source identity before testing;
- prove required tests did not rewrite tracked source after testing;
- retain bounded, non-secret evidence artifacts where useful;
- bind workflow/Action identities into the canary receipt so supply-chain changes invalidate stale evidence.

## Stale and red PR handling

A stale or conflicted canary PR is not disposable. Before closing it:

1. compare it with current `main` and relevant successor work;
2. identify unique still-valid tests, invariants, fixtures and documentation;
3. carry useful pieces onto a fresh branch from current `main` without rebase/reset/force-push;
4. preserve stronger current-main controls rather than choosing the stale side wholesale;
5. open and execute the successor PR;
6. close the old PR only after its unique useful work is reachable in the successor or proven already present elsewhere.

This document itself follows that procedure: the useful policy from PR #62 is salvaged onto current `main` instead of conflict-forcing the stale branch.

## Promotion checklist

Before promotion, require all of the following that apply:

- exact immutable source and tool revisions recorded;
- source repository required checks executed and passed;
- independent TypeSpec/JSON Schema admission executed and passed through pinned TJSV;
- native/runtime consumers executed for required language/runtime targets;
- adversarial/negative controls executed;
- format/lint/reproducibility checks passed;
- dependency locks/manifests are reproducible or explicitly reviewed and committed;
- checked source stayed immutable during validation;
- test-org canaries target the exact candidate closure;
- no required job is skipped, zero-step, runnerless, startup-failed or stale;
- current merge/base relationship is rechecked;
- merged production head is requalified when the merge commit differs from the tested PR head.

Only then should the candidate be described as promoted or certified.