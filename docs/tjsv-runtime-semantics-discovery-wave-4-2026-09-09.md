# TJSV runtime-semantics discovery wave 4 — 2026-09-09

Tracking: Linear `DEN-3959`, `DEN-3830`, `DEN-3828`; GitHub program `ORESoftware/.github#36`.

## Purpose

Continue the TJSV language/runtime-boundary audit without creating an unbounded backlog. The current audit budget is three new TJSV tasks per discovery wave under `ORESoftware/.github#107`. Deduplication searches are required before each task is opened; once the budget is reached, additional findings remain roadmap candidates rather than automatically becoming issues.

TypeSpec and independently human-authored JSON Schema/OpenAPI remain peer top-level authorities. Generated Schema B, Contract IR, runtime validators, direct schema evaluators, generated clients, transport traces and receipts are downstream evidence only. An unexplained discrepancy remains `STOPPED_FOR_EVALUATION`.

## Capped task set

The three slots for this wave are now occupied:

1. `#153` — **Define cross-runtime Unicode string length and normalization semantics.**
   - Make Draft 2020-12 code-point length explicit instead of inheriting UTF-16 code-unit, UTF-8 byte, or grapheme-count behavior from a runtime.
   - Distinguish exact JSON string identity from optional explicitly authored NFC/NFD normalization and from UI-only grapheme constraints.
   - Reuse `#65` for accepted-output evidence, `#90` for independent evaluators, `#70` for `format`, and `#140` for regex/pattern behavior.

2. `#154` — **Add cross-runtime streaming frame and termination semantics admission.**
   - Own parsed stream framing/control/terminal semantics between parsed HTTP response evidence (`#88`) and live transport/browser evidence (`#38`).
   - Cover ordering, heartbeats, typed terminal/error frames, truncation, cancellation and unsupported framing capabilities without promoting a transport projection to authority.

3. `#155` — **Prove JSON Schema `uniqueItems` and structural equality parity across runtimes.**
   - Prevent native object identity, `Set`, unstable serialization, map-key ordering or lossy numeric coercion from defining schema equality.
   - Coordinate numeric equality with `#137`, Unicode string identity with `#153`, direct evaluators with `#90`, and bounded mutation/property coverage with `#63`/`#81`.

These complement the immediately preceding semantic tasks already opened under the same program: `#137` numeric representation/precision, `#138` union/discriminator parity, `#139` repeat-run determinism, and `#140` portable pattern/regex semantics.

## Deferred discoveries after the task budget

The following searches found no focused open task, but they are deliberately **not** being opened in this audit because `#107`'s three-task budget is exhausted:

- **Object evaluation semantics:** `properties`, `patternProperties`, `propertyNames`, `additionalProperties`, and especially `unevaluatedProperties` across `allOf`/`oneOf`/conditionals/references. A future task should prove that evaluated-property annotations and overlapping pattern matches agree across generated validators and independent Draft 2020-12 evaluators. Pattern syntax itself remains owned by `#140`.
- **Array applicator/evaluation semantics:** `prefixItems`, `items`, `contains`, `minContains`, `maxContains`, and `unevaluatedItems`, including annotations that cross applicators/references. A future task should distinguish tuple/item validation from `uniqueItems` equality and reject runtimes that simplify away evaluation semantics.

Before either candidate becomes a task, rerun deduplication because this program is changing concurrently.

## Immediate execution order

1. Resolve the current `ORESoftware/typespec-json-schema-validator#77` conflict against current `main` semantically; do not rebase, reset, stash, force-push, or pick one side wholesale. Re-run the exact required Ubuntu/macOS/flags-2-env/compiler/package gates at the resulting head before merge.
2. Land validator-local provenance hardening in `typespec-json-schema-validator#78` (reverify language-boundary admission against canonical current inputs) and `#79` (keep the public boundary schemas and executable verifier in lockstep).
3. Use `#65` plus reusable admission `#37/#76` as the evidence substrate for `#137`, `#138`, `#140`, `#153`, and `#155`; avoid one-off per-runtime harnesses.
4. Layer parsed stream semantics `#154` over current-input-verified Contract IR/runtime evidence before claiming live transport coverage in `#38`.
5. Require repeat-run determinism from `#139` for assurance profiles that will feed fleet aggregation `#60` or release promotion `#57`.

## Evidence and promotion rule

A green result is meaningful only for the exact named assurance profile, source closure, Contract IR, corpus, runtime/toolchain/platform identities and retained receipt. Missing, stale, unsupported, zero-step, nondeterministic, over-budget or mismatched required evidence is not a pass. Higher-level transport, build, cohort, fleet and release receipts may consume lower-level evidence, but they must not silently strengthen what that evidence proved.

## Linear synchronization

New dedicated Linear child creation remains blocked by the current workspace issue-count limit. Do not invent DEN identifiers. Until capacity returns, the GitHub issues above are the executable task records; `DEN-3830`/`DEN-3959` and their linked planning documents are the Linear-side coordination records. `ORESoftware/.github#130` owns duplicate-safe backfill once capacity is restored.
