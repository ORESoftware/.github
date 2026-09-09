# TJSV source-revision and Lambda adversarial execution checkpoint — 2026-09-09

Tracking: Linear `DEN-3830`, `DEN-3959`; GitHub parent `ORESoftware/.github#36`.

This checkpoint records implementation evidence and bounded follow-up work. It does not claim fleet-wide rollout completion.

## Authority invariant

- Independently authored TypeSpec and independently authored JSON Schema/OpenAPI remain peer editable authorities.
- TypeSpec-generated Schema B, Contract IR, runtime artifacts, package output, receipts, and canary evidence remain downstream evidence only.
- Generated evidence cannot overwrite an authored authority or win a disagreement by fallback.
- Any unexplained mismatch remains `STOPPED_FOR_EVALUATION`.

## Verified TJSV implementation evidence

### Source-revision coherence — PR #83

`ORESoftware/typespec-json-schema-validator#83` merged at `b34cdf2538384b3b4f36b68f5ca430f92c396e72`.

The verifier now rejects supplied runtime evidence assembled from different valid immutable 40-hex source revisions with `boundary-source-revision-mismatch`. The rule applies to required evidence and to optional evidence when optional evidence is supplied; a mismatched witness is not counted as admitted evidence.

The final exact PR head was `e084496505a751baf311a3dd72d76200ed8fdcb5`. It passed Ubuntu 24.04 and macOS 14 CI run `34392320790`, including production dependency audit, syntax/CLI/unit/compiler-backed integration tests, package-boundary checks, and clean-consumer release preflight. The exact merge SHA passed post-merge `main` push CI run `34392540474`.

A concurrent hardening PR advanced `main` while #83 was open. The conflict was resolved semantically with a normal two-parent merge, preserving the newer incomplete-differential, incomplete-Contract-IR-scope, and retained-parity-findings negative controls plus the source-revision checks. No rebase, reset, stash, force-push, or blanket side selection was used.

### Expanded Lambda adversarial coverage — PR #85

`ORESoftware/typespec-json-schema-validator#85` merged at `bba0b123d2f25bb1b6a2c1470f1c3ab44f588bef` after semantic current-main reconciliation at exact head `9fe41bc8d18f669aee9b1c0008f4c7b68bcf7522`.

The Lambda regression profile now includes eight differential instances covering valid AWS Lambda, Cloudflare Workers, and Vercel commands plus invalid unknown operation/provider, missing required request ID, wrong schema version, and extra-property cases. It also adds 11 adversarial runtime-evidence mutations covering evidence schema identity, status, runtime identity, revision format, digest format, toolchain/generator identity, ingress/egress validation state, parity-receipt binding, and Contract-IR binding.

Exact-head CI run `34392864335` passed Ubuntu 24.04 and macOS 14, including clean package-consumer acceptance. The exact merge SHA then passed the same Ubuntu/macOS post-merge `main` jobs in run `34393072797`.

## Not merge-ready

### Current-input promotion entrypoint — PR #86

`ORESoftware/typespec-json-schema-validator#86` is intentionally not merged. Exact head `0d96b680cc6e2c0c94b31dc2617a39e74cb683c6` failed the core syntax/CLI/unit/compiler-backed gate on both Ubuntu 24.04 and macOS 14 in run `34392521130`; package acceptance was skipped. It must be fixed and reconciled against current main before it can be considered promotion evidence.

### Release-package preflight salvage — PR #87

`ORESoftware/typespec-json-schema-validator#87` remains open. Its own merge contract requires two review rounds at the exact green head. That review evidence is not present, so it must not be merged merely because the branch is mechanically mergeable.

## Newly refined bounded tasks

The rollout audit is already under the creation budget in `ORESoftware/.github#107`, so these refinements stay under existing canonical owners rather than creating duplicate issue clusters.

1. **Prove merge-result/current-base admission.** Distinguish `exact_head_ci_passed` from `merge_tree_verified` and `post_merge_verified`. A PR head green against an older base is insufficient after mainline semantic hardening.
2. **Bind one exact source closure across the full evidence graph.** Extend witness-to-witness source-revision coherence to parity/current-input receipt, Contract IR, consumer lock, runtime/package artifact digests, and toolchain identities. Add a cross-revision splice canary assembled from individually valid evidence from two commits and require fail-closed refusal.
3. **Promote validator revisions through compatibility review, not latest-wins.** Feed exact verified validator SHAs through `.github#75/#77` compatibility and consumer-lock policy before bounded Lambda tranches in `.github#168`; never mass-repin from a symbolic/latest reference.
4. **Repair #86 without weakening admission.** Diagnose its cross-platform core-gate failure, preserve the current-input re-verification design, reconcile with #83/#85, then require exact-head and post-merge proof.
5. **Keep package-surface proof separate from source/runtime proof.** #87's clean-consumer release preflight is complementary evidence and must retain its review requirement; package importability cannot substitute for source-closure/runtime validation.

## Cross-system mirrors

- `ORESoftware/.github#36` carries the parent rollout checklist and the merge-result/source-closure refinements.
- `ORESoftware/.github#131` carries the cross-revision runtime-witness negative-control refinement.
- `ORESoftware/.github#168` carries the bounded Lambda candidate-pin follow-through and explicitly forbids blind mass repinning.
- Linear document `TJSV language-boundary rollout work breakdown — DEN-3830 — 2026-09-09` contains the same implementation and task evidence.
- Linear `DEN-3959` contains the execution update linking the merged validator evidence to the Lambda rollout work.

## Promotion stop conditions added by this checkpoint

- Runtime witnesses name different immutable source revisions.
- A green PR head has not been reconciled/tested against the current base after relevant mainline changes.
- Exact post-merge CI is missing, skipped, zero-step, cancelled, or failing.
- A candidate validator revision bypasses compatibility/consumer-lock review.
- Current-input verification or clean package-consumer evidence is red or skipped when the active assurance profile requires it.

This document is coordination evidence only. The exact implementation and CI records above remain the source for implementation state.