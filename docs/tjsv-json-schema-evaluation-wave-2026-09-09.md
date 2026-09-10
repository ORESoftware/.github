# TJSV JSON Schema evaluation-semantics wave — 2026-09-09

Tracking: Linear `DEN-3830`, `DEN-3959`, `DEN-3828`; GitHub parent [`ORESoftware/.github#36`](https://github.com/ORESoftware/.github/issues/36).

This checkpoint records the bounded follow-up discovered after re-reading the current TJSV roadmap, the validator-local issue graph, and the Linear work breakdown. It supplements the existing rollout/runtime/evidence roadmaps; it does not replace their task ownership.

## Authority invariant

- Human-authored TypeSpec and human-authored JSON Schema/OpenAPI remain independent peer top-level authorities.
- `ORESoftware/typespec-json-schema-validator` (TJSV) is the required fail-closed convergence/admission implementation for applicable cross-language/runtime contract evidence.
- Generated Schema B, Contract IR, generated validators/clients, runtime observations, resolver traces, compatibility receipts, and fleet summaries are downstream evidence only.
- No generated artifact, runtime, validator majority, historical receipt, or fallback source may resolve an unexplained peer-authority discrepancy.
- Missing, stale, skipped, zero-step, unsupported, or semantically incomplete required evidence remains non-promotable.

## Deduplication result

The prior roadmap left three evaluation-semantics candidates for a later deduplicated pass. Fresh GitHub and Linear searches produced two new bounded owners and one reuse decision.

### Reference closure — reuse TJSV #8; do not duplicate

Canonical implementation owner: [`ORESoftware/typespec-json-schema-validator#8`](https://github.com/ORESoftware/typespec-json-schema-validator/issues/8).

That issue already owns the material semantic boundary: Draft 2020-12 resource graphs, nested `$id` scopes, `$anchor`, `$dynamicAnchor`, `$ref`, `$dynamicRef`, base/resource identity, pinned offline catalogs, cycles, identifier/anchor collisions, deterministic resolution traces, and fail-closed missing/ambiguous resources. The account-level roadmap therefore must not create a second reference-resolution engine or issue.

The residual integration requirement is to consume #8's exact-current resolver evidence through the existing TJSV assurance/admission path and feed it to runtime/fleet/release gates without turning the resolver receipt into a third authority.

### Array evaluation — new `.github#192`

[`ORESoftware/.github#192`](https://github.com/ORESoftware/.github/issues/192) owns Draft 2020-12 `prefixItems`, `items`, `contains`, `minContains`, `maxContains`, and `unevaluatedItems` parity, including evaluated-index annotation propagation through composition.

It is intentionally separate from [`#155`](https://github.com/ORESoftware/.github/issues/155), which owns `uniqueItems` and structural JSON equality.

### Object evaluation — new `.github#193`

[`ORESoftware/.github#193`](https://github.com/ORESoftware/.github/issues/193) owns `properties`, `patternProperties`, `additionalProperties`, `unevaluatedProperties`, `propertyNames`, `dependentRequired`, and `dependentSchemas`, including evaluated-property annotation propagation through composition.

It coordinates with [`#140`](https://github.com/ORESoftware/.github/issues/140) for portable regex semantics rather than defining another regex profile, and remains distinct from [`#138`](https://github.com/ORESoftware/.github/issues/138) discriminator/tagged-union behavior.

## Recommended dependency order

1. Stabilize exact-current evidence and resolver closure: TJSV #8, the current-input/schema lockstep work, and the named assurance vocabulary.
2. Keep execution bounded and non-vacuous: `.github#81`, `#63`, and validator diversity in `#90`.
3. Land scalar/string prerequisites where the structural semantics depend on them: numeric profile `#137`, Unicode/string profile `#153`, and portable regex profile `#140`.
4. Execute array/object evaluation semantics: `#192`, `#193`, together with structural equality `#155` and discriminator behavior `#138` where fixtures overlap.
5. Run required native/runtime matrices and normalized evidence under the reusable TJSV admission path.
6. Feed exact-current semantic receipts through repeat-run determinism, compatibility/version-policy, dependency-cohort, release, and fleet gates (`#139`, `#85`, `#135`, `#136`, `#57`, `#60`) without creating a second parity engine.

## Stop conditions

Promotion must stop when any required evaluator/runtime:

- resolves a different resource closure or cannot prove the exact resource identities it used;
- loses or invents evaluated array indexes or object properties through composition;
- approximates `unevaluatedItems` as ordinary `items` or `unevaluatedProperties` as `additionalProperties` when the evaluation state differs;
- silently skips unsupported keywords or falls back to a weaker validator/profile;
- disagrees with another required evaluator/runtime on the retained corpus;
- presents evidence for a different authored-source, TJSV, runtime, toolchain, or fixture revision; or
- has a zero-step/skipped runner result instead of executed evidence.

All such cases remain `STOPPED_FOR_EVALUATION` with bounded deterministic evidence; no majority vote or source precedence resolves the discrepancy automatically.

## Task-creation budget

This pass declared a maximum of three possible new tasks, in line with `.github#107`.

- one candidate was deduplicated to existing TJSV #8;
- two materially distinct tasks were created as `.github#192` and `.github#193`;
- no fourth adjacent task was created.

## Linear synchronization

Linear child-issue creation is still constrained by the workspace issue-count limit recorded in the existing DEN-3830 planning document. The executable tasks therefore live in GitHub while the canonical Linear document `TJSV language-boundary rollout work breakdown — DEN-3830 — 2026-09-09` mirrors this ownership decision. Existing Linear issues `DEN-3830`, `DEN-3959`, and `DEN-3828` remain the broader cross-system contexts; no synthetic DEN identifier is invented.

This file is planning/ownership evidence only. It does not mark TJSV #8, #192, #193, any runtime matrix, release gate, or fleet rollout complete without exact-head executed evidence.
