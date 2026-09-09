# OWLS next-step execution ledger — 2026-09-09

Linear umbrella: [DEN-3959](https://linear.app/denman/issue/DEN-3959/adopt-dual-typespec-and-json-schemaopenapi-authorities-and-enforce)  
Linear project: `ores-wasm-loaders`

This is an execution ledger, not a new contract authority and not a production-rollout approval. The Linear workspace currently rejects new issue creation at its free issue limit, so OWLS work is tracked with GitHub tasks plus the existing DEN-3959/project discussion until a dedicated Linear issue can be created without duplicating history.

## Current exact evidence

- Contract authority: `ores-wasm-loaders/owls-interfaces@cfe0b18fe9ae361d94ea0646627cb732465b5496` models optional `Asset.dependencies`, dependency-graph coherence, and dependency-closure helpers. TypeSpec and hand-authored JSON Schema remain independent editable peer authorities; Schema B, Contract IR, language projections, and receipts remain evidence only.
- Browser loader: `ores-wasm-loaders/owls-web-loader@d9f7624c80b606e8be5479f9e2dea89ac9e35284` merged dependency-aware route preparation. Its exact head passed Contract-IR/TJSV consumer, loader, and Zed-candidate gates before merge.
- Native Rust: previous merged head `a4f996544aff9004988c8fa76fbadc2d8fede555` certifies the pre-DAG `76364a...` interface generation. PR `owls-runtime.rs#10` is the active DAG-admission update.
- Flutter: previous merged head `ea2ca9c274d386fc68e2cf72412d015b88df4774` certifies the pre-DAG current interface generation while keeping its released 0.1.1 dependency pin separate. PR `owls-flutter#8` is the active DAG-admission update.
- Independent external closure: `ores-wasm-loaders-test/owls-e2e#9` merged a five-host exact-source closure for the prior `76364a...` generation and passed contract, 54-case external matrix, controls, marketing-browser ownership, and real Leptos/Flutter browser gates. Preserve it as historical evidence; refresh rather than rewrite it after the two host updates merge.
- Real Dioxus acceptance is not yet equivalent to current manifest/DAG conformance. The current independent E2E tree contains real Leptos and Flutter fixtures; no checked-in real Dioxus SDK application/toolchain path was found in the current discovery pass.

## Execution order

### P0 — close the current contract generation

1. **Native Rust DAG admission — `.github#102`**  
   https://github.com/ORESoftware/.github/issues/102  
   Active implementation: https://github.com/ores-wasm-loaders/owls-runtime.rs/pull/10  
   Require exact `cfe0b18...` current interface admission, audited TJSV, canonical fixture/Contract-IR evidence, Rust fmt/Clippy/tests, and no expansion of native capabilities.

2. **Flutter DAG admission — `.github#104`**  
   https://github.com/ORESoftware/.github/issues/104  
   Active implementation: https://github.com/ores-wasm-loaders/owls-flutter/pull/8  
   Advance only the current-compatibility interface pin. Keep the released-package pin frozen and require full fixture round-trip so `dependencies` cannot disappear at the Dart boundary.

3. **Refresh five-host external closure — `.github#106`**  
   https://github.com/ORESoftware/.github/issues/106  
   Start only after #102 and #104 merge. Pin one coherent interface/TJSV/browser/native/Flutter source generation and rerun contract admission, 54-case corpus, controls, marketing ownership, and real-framework/browser matrices.

### P1 — qualify the remaining acceptance surfaces independently

4. **Real Dioxus split-route browser build — `.github#108`**  
   https://github.com/ORESoftware/.github/issues/108  
   Build an actual pinned Dioxus application, inventory real emitted split Wasm, generate the dependency DAG through the Rust manifest tool, admit it through TJSV/Contract IR, and test real route navigation/failure behavior across browsers. Do not create a second splitter.

5. **Remote immutable publication and portable locks — `.github#110`**  
   https://github.com/ORESoftware/.github/issues/110  
   Move from isolated/frozen candidate installs to reviewed immutable releases, portable locks, clean external consumption, stale-document compatibility, and release rollback provenance. Publication is not production enablement.

6. **Actual ores-otel + field evidence — `.github#111`**  
   https://github.com/ORESoftware/.github/issues/111  
   Wire representative Rust/Leptos and Flutter products to bounded OWLS telemetry, preserve downloaded/runtime-ready/useful-interaction distinctions, and collect preregistered field measurements. Lab or synthetic data cannot satisfy the field gate.

7. **Production-origin/auth/CSP/CORS + physical mobile — `.github#112`**  
   https://github.com/ORESoftware/.github/issues/112  
   Test real boundary semantics without merging origins for performance. Cover authentication, CSP/CORS/isolation, credentialless preparation, physical iOS/Android, no-hover behavior, lifecycle/fallback, and exact device/release evidence.

### P2 — rollout decision, not automatic rollout

8. **Rollback drill and evidence-backed fleet decision — `.github#113`**  
   https://github.com/ORESoftware/.github/issues/113  
   Exercise kill switches and immutable-release rollback, bind the decision receipt to exact packages/sources/devices/deployments, retain controls, and require explicit reviewed approval before 35+ organization expansion. Automated analysis may yield eligibility for review but cannot self-authorize production rollout.

## Dependency graph

```text
#102 native DAG ─┐
                 ├─> #106 refreshed five-host closure ─┐
#104 Flutter DAG ┘                                    │
                                                      ├─> #113 rollback / rollout decision
#108 real Dioxus ─────────────────────────────────────┤
#110 publication ─────────────────────────────────────┤
#111 ores-otel field evidence ────────────────────────┤
#112 production/mobile topology ──────────────────────┘
```

The P1 gates may proceed in parallel after their prerequisites are available. A pass in one lane never substitutes for another lane's evidence.

## Evidence and merge rules

- Use `DEN-3959` in active branches/PR titles while the issue quota prevents a more specific Linear issue.
- Every source pin and GitHub Action used for admission must be immutable and verified at runtime.
- TJSV must continue to enforce convergence between independently authored TypeSpec and JSON Schema authorities; no generated artifact gains editable-authority status.
- Do not rebase, stash, reset, force-push, or discard concurrent work. Merge current default branches semantically and rerun exact-head gates after reconciliation.
- Do not mark a draft, missing, skipped, cancelled, stale, or infrastructure-failed gate as passing.
- Keep released-package compatibility separate from current-head compatibility until publication actually occurs.
- Preserve previous exact-source receipts as history; supersede them additively rather than mutating old evidence.
- No credential from chat, Git history, issue text, or repository files is an authentication fallback. Use configured clients/approved secret channels; do not revoke or rotate credentials without explicit authorization.
