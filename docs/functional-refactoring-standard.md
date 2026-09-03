# Functional refactoring standard

Tracking: [ORESoftware/.github#19](https://github.com/ORESoftware/.github/issues/19) · Linear: `DEN-4255`

## Purpose

Move highly imperative code toward smaller pure decision functions and explicit effect adapters **without** rewriting stable systems for style alone. The goal is deterministic behavior, easier tests, safer concurrency, and clearer failure handling—not functional-programming dogma or a new framework mandate.

A refactor is successful only when externally observable behavior is preserved or an intentional behavior change is separately specified and tested.

## Default architecture

Use a **functional core / imperative shell**:

```text
untrusted input
  -> parse and validate
  -> immutable domain value
  -> pure decision/transition functions
  -> explicit effect plan
  -> narrow adapter executes effects
  -> normalized result/event
```

Pure code must not read environment variables, clocks, random sources, process-global state, files, networks, databases, UI state, loggers, or provider SDKs directly. Supply those values as explicit inputs. Effect adapters own I/O and return typed results; they do not choose product policy.

This boundary applies across TypeScript/JavaScript, Rust, Go, Gleam/Erlang/Elixir, Dart, and other languages in the portfolio, using language-idiomatic types rather than forced emulation of another language.

## Admission rules

Before opening a broad refactor PR:

1. Name the concrete problem: nondeterministic tests, tangled effects, unsafe shared mutation, duplicate validation, hard-to-review control flow, unreliable retries, or another measured defect.
2. Capture current behavior with characterization tests at the public boundary.
3. Identify the authoritative contracts, generated artifacts, downstream consumers, and cross-repository dependencies.
4. Define the smallest pure seam that can be extracted without a flag-day rewrite.
5. Record which effects remain and which adapter owns them.
6. Separate behavior changes from structural changes whenever practical.
7. Keep the existing public API unless a migration plan, compatibility period, and consumer evidence justify changing it.

“Make it functional” without a named behavior/risk and verification plan is not an actionable fleet issue.

## Pure decision functions

A pure decision function:

- returns the same value for the same complete input;
- does not mutate arguments or shared state;
- does not perform I/O;
- represents expected failure as a typed value rather than an uncaught process-global exception;
- returns a new domain value or an explicit effect plan;
- accepts clock/randomness/configuration as data when policy depends on them;
- is bounded for untrusted input and does not hide unbounded recursion or allocation.

Prefer total functions over partial functions at contract boundaries. When an input is invalid or unsupported, return a closed error variant. Do not silently coerce unknown cases into a default that can trigger an effect.

## State transitions

Model nontrivial lifecycle logic as an explicit state machine:

```text
next = transition(current_state, event, policy)
```

The transition function returns one of:

- the next immutable state plus zero or more effect intents;
- a typed rejection explaining why the event is invalid;
- a discrepancy/stop state when independent authorities disagree.

Persist the accepted transition before or atomically with externally visible effects where the domain requires it. Retry logic must be defined at the effect boundary and tied to an idempotency key; a pure transition must not retry I/O internally.

Illegal transitions, duplicate events, stale revisions, and concurrent-update conflicts require tests. “Last writer wins” is not an implicit default.

## Effects as data

Represent effects as a closed plan where this improves safety and testability:

```text
Decision {
  state,
  effects: [WriteRecord(...), PublishEvent(...), ScheduleRetry(...)]
}
```

The adapter validates that every effect is permitted for the caller and current revision before execution. Unknown effect variants fail closed. Effect payloads must contain references or digests instead of credentials and unnecessary sensitive data.

Do not turn every local call into an abstract effect. Use this pattern where effects cross trust, concurrency, persistence, provider, or failure boundaries.

## Error handling

Use typed, bounded errors at module and service boundaries. Separate:

- invalid input;
- policy denial;
- conflict/stale revision;
- unavailable dependency;
- timeout/cancellation;
- resource exhaustion;
- discrepancy between independent authorities;
- unexpected internal failure.

Do not encode expected control flow by parsing free-form error messages. Do not catch an error merely to log and continue when state may be partial. Preserve causes internally, but redact credentials, personal data, provider payloads, and filesystem details from public errors and telemetry.

## Collections and iteration

Prefer transformations whose ordering and cardinality are explicit. `map`, `filter`, `fold`, iterators, comprehensions, and pipelines are useful when they clarify data flow; ordinary loops are acceptable when they are clearer or avoid unnecessary allocations.

Avoid replacing a readable bounded loop with a dense chain that hides side effects, error short-circuiting, ordering, or complexity. Side effects inside `map`/`filter` callbacks are prohibited unless the API is explicitly an effect iterator and the ordering/failure semantics are documented.

## Immutability and performance

Default to immutable domain values at module boundaries. Local mutation inside a proven pure implementation is allowed when it is encapsulated, unobservable, and materially improves performance or clarity.

Do not introduce expensive full-copy behavior, persistent data structures, recursion, boxing, or allocations without measurement in hot paths. A functional interface and an efficient mutable implementation can coexist.

Performance claims require a representative benchmark with inputs, platform, warm-up, variance, and before/after results. Do not sacrifice correctness or cancellation for benchmark wins.

## Concurrency

Pure decision code should be independent of task scheduling. Effect adapters own concurrency and must define:

- maximum parallelism and queue bounds;
- ordering guarantees;
- cancellation propagation;
- timeout ownership;
- retry and idempotency behavior;
- partial failure semantics;
- shutdown/drain behavior;
- conflict detection and compare-and-set/fencing where required.

Never share mutable process-global request context. Pass context explicitly or use a language-native scoped context mechanism that cannot leak between requests; request/user identifiers belong in structured context, not hidden globals.

## Configuration and flags

Parse argv/environment exactly once at the process boundary using the repository's reviewed flags-2-env contract where applicable. Convert external strings into a validated immutable configuration value. Pure code receives that value; it does not call `process.env`, `std::env`, or equivalent throughout the domain layer.

Defaults never override an explicitly supplied environment or flag. Unknown fields and invalid combinations fail closed. Credentials are references supplied by the runtime secret boundary, not values in configuration fixtures or generated documentation.

## Contracts and generated artifacts

TypeSpec and JSON Schema/OpenAPI remain independent, human-authored, top-level authorities where both apply. Functional refactoring must not collapse either into a generated subordinate source.

Normalize and compare their relevant type/operation/persistence witnesses. Unexplained discrepancies stop generation/promotion. Diesel and SeaORM outputs likewise cross-check each other; a refactor may not choose one silently because its job completed first.

Edit authoritative sources and rerun generators. Do not hand-edit derived clients, schemas, SQL, or ORM projections to make a refactor appear green.

## Language guidance

### TypeScript / JavaScript

- parse untrusted `unknown` once into narrow domain types;
- avoid module-level mutable singletons for request state;
- prefer discriminated unions for states/results/effects;
- inject clocks, randomness, fetch, storage, and logger interfaces;
- avoid promise creation inside reducers unless the reducer explicitly returns an effect plan;
- preserve stack/cause internally and emit structured bounded errors.

### Rust

- use enums for states/results/effects and newtypes for validated identifiers;
- keep async/network/database work outside pure transition modules;
- prefer borrowing and iterators when clear, but allow encapsulated mutable buffers in hot paths;
- never `unwrap`/`expect` on untrusted runtime paths merely to simplify a refactor;
- test property/invariant boundaries as well as examples.

### Go

- use small explicit data types and pure functions rather than framework-heavy abstractions;
- pass `context.Context` only to operations that can block or be cancelled, not as an untyped value bag for domain policy;
- return typed/sentinel errors or result values with stable classification;
- avoid package-level mutable configuration and clients;
- preserve clear loops when higher-order helpers would obscure allocation or error flow.

### Gleam / Erlang / Elixir

- keep message handling as explicit state transitions;
- isolate ports, files, network calls, timers, and process supervision from pure decision modules;
- define mailbox/backpressure and restart semantics;
- do not equate process isolation with authorization or input validation.

### Dart / Flutter

- keep widgets/view models from owning provider/network policy;
- use immutable view state and explicit events/effects;
- place platform-specific effects behind adapters so mobile and desktop behavior stays semantically aligned;
- test pure state transitions without a device or widget tree where possible.

## Refactoring sequence

Use an incremental sequence:

1. add characterization tests;
2. introduce validated input/domain types;
3. extract one pure decision or transition seam;
4. make effects explicit and route them through a narrow adapter;
5. add differential tests comparing old and new paths over fixtures/properties;
6. switch one call site or canary;
7. remove the old path only after consumer evidence and rollback criteria are satisfied;
8. repeat.

Keep each PR reviewable. A mechanical rename/format pass should not be mixed with semantic transition changes, dependency upgrades, schema migrations, or deployment changes.

## Required evidence

A functional-refactor PR must state:

- problem and scope;
- public behavior preserved or intentionally changed;
- pure core and effect adapters introduced;
- state/error/effect contracts;
- tests and exact commands actually run;
- differential/property/fault-injection evidence where applicable;
- performance result or explicit “not performance-sensitive” rationale;
- migration, rollback, and downstream-consumer status;
- unresolved discrepancies or stop conditions;
- security/privacy impact.

Hosted CI status is reported separately from local checks. Do not call a refactor complete merely because it compiles.

## Anti-patterns

Reject or revise PRs that:

- replace a working subsystem wholesale without characterization tests;
- hide I/O in constructors, getters, reducers, collection callbacks, or global initializers;
- use a generic `Map<String, Any>` / `Record<string, unknown>` as a permanent domain model;
- make every function generic/curried or introduce a framework with no measured need;
- swallow errors to keep a pipeline flowing;
- perform unbounded parallel mapping;
- turn independent authorities into a precedence chain;
- hand-edit generated artifacts;
- mix refactor and feature behavior without a differential plan;
- claim purity while reading clocks, randomness, environment, global context, or caches implicitly;
- expose secrets or personal data in fixtures, logs, effect plans, or receipts.

## Completion

Portfolio-wide completion is measured repository by repository. Each target requires an issue/PR with a bounded behavior, tests, and evidence. This document is the shared standard; it is not evidence that every repository has already been refactored.
