# OWLS shared WASM loader — next-wave execution plan

Date: 2026-09-09  
Tracking: Linear `DEN-3959`, projects `ores-wasm-loaders` and `ores-wasm-loaders-test`

## Purpose

This document is the durable cross-repository backlog for the OWLS shared WebAssembly loading platform. GitHub remains authoritative for commits, pull requests, workflow results, releases, and deployment evidence; Linear remains authoritative for work status and prioritization.

The contract model is invariant:

- human-authored TypeSpec and human-authored JSON Schema Draft 2020-12 are independent peer authorities with no precedence;
- `ORESoftware/typespec-json-schema-validator` (TJSV) is the required admission boundary for cross-language/runtime contracts;
- generated Schema B, Contract IR, projections, and consumer receipts are derived evidence, never a third editable authority;
- no consumer may use a mutable TJSV ref;
- every cross-runtime consumer must verify the exact admitted interface revision, TJSV revision, source digests, complete declaration scope, and runtime fixture corpus.

## Current audited state

Latest merged core revisions at the time of this plan:

| Component | Revision | Evidence |
| --- | --- | --- |
| TJSV | `03ccc0ecdfc70f9198c3ccf80718910961d3fde1` | reviewed immutable validator/action revision |
| `owls-interfaces` | `cfe0b18fe9ae361d94ea0646627cb732465b5496` | dependency-DAG contract admitted by PR #14; exact-head contract run `34314295711` |
| `owls-web-loader` | `d9f7624c80b606e8be5479f9e2dea89ac9e35284` | route-dependency prefetch from PR #24; exact-head test/TJSV/Zed runs `34367271589`, `34367271601`, `34367271571` |
| `owls-runtime.rs` | `a4f996544aff9004988c8fa76fbadc2d8fede555` | current TJSV host admission, still pinned to the preceding interface revision |
| `owls-flutter` | `ea2ca9c274d386fc68e2cf72412d015b88df4774` | current TJSV host admission, current-contract lane still pinned to the preceding interface revision |
| `owls-e2e` | `c9a01743f554c126f04231b8da38c4a59d265390` | five-host closure and real browser matrix, now behind the dependency-DAG interface/web-loader heads |

The immediate drift is intentional only until WL-17 completes: native, Flutter, and E2E must advance to `cfe0b18...` / `d9f7624...` and re-certify the complete closure.

## Implementation backlog

### WL-17 — Propagate the dependency-DAG contract through every host

**Repositories:** `owls-runtime.rs`, `owls-flutter`, `owls-e2e`  
**Priority:** P0

- advance native and Flutter current-contract lanes to `owls-interfaces@cfe0b18...`;
- advance E2E to `owls-interfaces@cfe0b18...` and `owls-web-loader@d9f7624...` plus the resulting native/Flutter merge commits;
- retain TJSV `03ccc0...`, fixture corpus, canonical complete-scope verifier, language projection checks, and immutable five-host source closure;
- add regression coverage proving `Asset.dependencies` round-trips in every host even when the host does not itself execute route splitting.

**Acceptance:** all host PR exact-head jobs green; five E2E workflows green on one immutable closure; no mutable refs; no production rollout implied.

### WL-18 — Verify real Dioxus split output, not inferred filenames

**Repositories:** `owls-web-loader`, `owls-e2e`  
**Priority:** P0

Build a pinned Dioxus 0.7.x application with real route splitting and derive dependency edges from generated framework output such as `__wasm_split.js` or equivalent emitted metadata. Feed those paths through the Rust manifest builder and prove that the resulting `Asset.dependencies` graph matches actual emitted files.

**Acceptance:** missing, duplicate, self, cyclic, disconnected, or guessed filename edges fail closed; browser test proves route prefetch warms the real dependency closure without application execution.

### WL-19 — Integrate `prefetchRoute()` into marketing and persistent-shell navigation

**Repositories:** `owls-web-loader`, first pilot marketing/app repos  
**Priority:** P0

- expose route-intent preparation through the existing HTML/Astro link integration;
- preserve ordinary href behavior, modified clicks, keyboard navigation, and full-page fallback;
- acquire activation ownership before releasing speculative route work;
- do not initialize Flutter, Leptos, Dioxus, authentication, subscriptions, or private data during preparation.

**Acceptance:** A/B/C/D controls remain valid and tests distinguish route-prefetch benefit from persistent-document benefit.

### WL-20 — Publish immutable remote Zed releases and portable locks

**Repositories:** `owls-interfaces`, `owls-web-loader`, `owls-runtime.rs`, `owls-flutter`, consumer fixtures  
**Priority:** P1

Replace isolated/local registry evidence with reviewed remote immutable publication. Generate portable locks containing immutable VCS/package provenance and verify a clean external consumer can install without sibling checkouts or `file://` registry assumptions.

**Acceptance:** published artifact digest + source commit + TJSV/interface closure retained; clean consumer CI resolves only published artifacts; rollback can select the prior immutable release.

### WL-21 — Define and wire production `ores-otel` loader telemetry

**Repositories:** `owls-interfaces`, `owls-web-loader`, `ores-otel`, pilot apps  
**Priority:** P1

Create independent TypeSpec and JSON Schema authorities for loader telemetry envelopes and admit them with TJSV. Record only bounded public identifiers and lifecycle metrics: preparation start/result, bytes, activation start/runtime ready/useful interaction, fallback mode, cancellation, and cohort. No URLs with query data, user IDs, tokens, or raw errors.

**Acceptance:** cross-language telemetry projections pass TJSV; real pilot exports trace/metric evidence; telemetry failure cannot break loading.

### WL-22 — Adaptive speculation budgets with deterministic ceilings

**Repositories:** `owls-web-loader`  
**Priority:** P1

Use explicit policy inputs such as save-data/network capability when available, historical asset sizes, and product-configured ceilings. Keep a deterministic hard cap per candidate, total in-flight bytes, concurrent candidates, and request count. Missing network hints must produce conservative behavior.

**Acceptance:** property/regression tests cover budget exhaustion, partial transfers, cancellation races, and unavailable browser hints; no unbounded speculative queue.

### WL-23 — Cache/origin topology certification

**Repositories:** `owls-e2e`, representative marketing/app repos  
**Priority:** P1

Certify same-origin paths, same-site subdomains, unrelated custom domains, and `github.io` partitioning separately. Do not assume a central CDN response fetched under one top-level site is reusable under another. Test HTTP cache behavior independently from optional Cache Storage/service-worker behavior.

**Acceptance:** network traces classify real transfers/revalidation; any service-worker path has an explicit read path, version/expiry policy, and rollback behavior.

### WL-24 — Atomic release selection and long-lived tab compatibility

**Repositories:** `owls-interfaces`, `owls-web-loader`, publishing/deployment workflows  
**Priority:** P1

- upload immutable assets before manifests/pointers;
- pin document/server hydration output to one release;
- retain prior assets long enough for open tabs and cached documents;
- prevent a newer mutable pointer from hot-swapping an incompatible running document.

**Acceptance:** deployment-during-session and stale-HTML tests pass with no mixed bootstrap/Wasm release.

### WL-25 — Security-header compatibility matrix

**Repositories:** `owls-e2e`, pilot application infrastructure  
**Priority:** P1

Test production-equivalent CSP, CORS, MIME, SRI, COOP/COEP, threaded Flutter rendering, authentication redirects, and third-party integrations. Do not broaden `unsafe-eval` or merge security origins merely for loader performance.

**Acceptance:** explicit supported header matrix; unsupported combinations fail closed or use documented framework fallback.

### WL-26 — Fleet adoption/audit command

**Repositories:** `ores-cli`, marketing/app fleet  
**Priority:** P2

Add an `oresc` audit for shared-loader adoption across the 35+ marketing/application sites: manifest contract revision, immutable package/source pins, TJSV admission evidence, intent policy, telemetry, cache/origin topology, and rollback controls. The audit is read-only by default; remediation must be explicit.

**Acceptance:** machine-readable JSON result plus human report; can distinguish compliant, partial, blocked, and not-applicable sites without inventing missing infrastructure.

## Independent acceptance backlog

### WT-09 — Real Dioxus route-split browser fixture

Build and test an actual Dioxus split application across supported browsers. Verify emitted dependency closure, dependency-first preparation, activation, route transitions, failure of one shared dependency, and repeated route visits.

### WT-10 — Physical mobile/browser coverage

Test at least one physical iOS/Safari and one physical Android/Chrome device for marketing intent, navigation fallback, Flutter web runtime selection, persistent-shell behavior, background/foreground restoration, and memory retention. Emulator/simulator evidence remains separate.

### WT-11 — Persistent-shell and mount/unmount soak

Run repeated Leptos/Dioxus/Flutter activation and cleanup cycles. Track live views, event listeners, subscriptions, DOM nodes, Wasm memories, and JS heaps after warm-up. Define an explicit acceptable stabilization envelope.

### WT-12 — Production-origin/authentication failure matrix

Exercise authenticated and unauthenticated entries, expired sessions, CSP/CORS/SRI/MIME failures, cross-origin redirects, stale manifests, partial deployment, and offline activation of already-loaded shells. Full-page offline navigation must not be claimed without an explicit offline mechanism.

### WT-13 — Field-performance statistical acceptance

Collect sufficient observations for A/B and C/D matched comparisons. Report sample size, p50/p75/p95, confidence interval or other preregistered uncertainty measure, activation reliability, marketing LCP/INP, and unused speculative bytes. Inconclusive data remains HOLD.

### WT-14 — Speculative-waste and cache-efficiency accounting

Measure prepared bytes that were never activated, bytes reused from HTTP cache, bytes revalidated, eviction, repeated-navigation savings, and per-framework/runtime-mode differences. Never infer a cache hit solely from `transferSize === 0` where timing restrictions can explain it.

### WT-15 — Release rollback drill

Deploy a non-production canary release, exercise preparation and activation, move the pointer back to the prior immutable release, and confirm old and new open tabs remain coherent. Record exact artifacts and recovery times; no destructive deletion of the newer release during the drill.

### WT-16 — 35+ site staged expansion gate

Expand only after prior acceptance gates pass: 2 pilot apps -> small mixed-framework cohort -> larger organization cohort -> fleet. Each stage needs an explicit stop/rollback criterion, independently reviewed evidence, and a preparation kill switch.

## Execution order

1. **WL-17** closure propagation.
2. **WL-18 + WT-09** real Dioxus emitted split graph.
3. **WL-19** marketing/persistent-shell route-intent integration.
4. **WL-20 + WL-21** remote package provenance and production telemetry.
5. **WL-22–WL-25 + WT-10–WT-15** policy, topology, security, devices, statistics, rollback.
6. **WL-26 + WT-16** fleet audit and staged adoption.

## Rules for completion

A task is not complete because code exists locally or one job is green. Completion requires pushed commits, a reviewed PR, exact-head required checks, and merge evidence. Cross-language contract changes additionally require TJSV admission from the exact independent TypeSpec and JSON Schema sources. Production rollout is a separate decision from implementation and test completion.
