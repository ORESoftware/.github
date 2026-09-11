# Functional immutability guidelines

ORES libraries and services should prefer value-producing transformations over mutation-oriented APIs when the extra allocation/copy cost is not material.

## Default rule

Prefer APIs that create and return a new value:

```text
next = transform(current)
```

instead of APIs whose primary effect is mutating caller-owned state:

```text
mutate(current)
```

The intent is deeper than shallow copying. New values should own newly constructed fields/collections where practical, so callers do not accidentally share mutable nested state.

## Rust

Prefer:

- constructors and `with_*` methods that return `Self` or a distinct output type;
- iterator pipelines plus `map`, `filter_map`, `fold`, `collect::<Result<...>>()`, and typed state transitions;
- immutable input references and owned outputs;
- typestate/generic wrappers where they make invalid states unrepresentable;
- enum/result transformations instead of out-parameters;
- fresh collections for transformed domain values rather than mutating caller-owned collections.

Avoid introducing `&mut T` parameters merely to return multiple effects. Return a struct/tuple/result instead. Local mutation inside a small constructor/collector is acceptable when it is clearly encapsulated and measurably simpler or faster.

## TypeScript / JavaScript / Bun / Deno

Prefer expression-oriented transforms (`map`, `filter`, `flatMap`, object/array construction, reducers that return new accumulators) to shared arrays/objects mutated with `push`, property assignment, or in-place sorting. Do not mutate caller-owned objects or arrays unless the API explicitly documents ownership transfer.

## Dart / Flutter

Prefer immutable models, `final` fields, value constructors, `copyWith` only when it creates independent nested values as required, collection transforms, sealed state transitions, and streams that emit new state objects. Avoid mutating a model after publication to widgets/Rx streams.

## Go

Prefer constructors and value-returning functions over pointer out-parameters. Use generic helpers where Go's type parameters fit cleanly; otherwise use typed constructors/methods that return new values. Pointer receivers remain appropriate for resource handles and measured hot paths, not merely as the default style.

## Gleam

Continue leaning on immutable data, pipelines, pattern matching, result/option composition, and record updates that produce new records.

## Hot-path exception

Mutation is allowed—and sometimes preferred—when profiling or algorithmic constraints show that repeated allocation/copying is material, including tight parsers, codecs, crypto buffers, network I/O buffers, large collection transforms, lock-free structures, or arena-backed systems.

When a non-obvious mutable implementation is intentionally retained for performance, add a nearby comment explaining:

1. what allocation/copy the mutation avoids;
2. why the path is performance-sensitive;
3. what ownership/aliasing invariant keeps the mutation safe;
4. what benchmark/profile should be consulted before converting it to an immutable implementation.

Do not add ritual comments to obvious kernel/I/O buffer mutation.

## Review guidance

Reviewers should flag mutation-oriented public APIs when an owned-result API is equally clear. Refactors must preserve behavior and should add regression tests that prove inputs are unchanged when relevant. Do not force immutability if it would materially regress a proven hot path.

Initial rollout targets include shared libraries and clients across `ores-*`, `ORESoftware/ores-*`, `opto-sync`, `fanwaave`, and `shared-auth`, including Rust, Go, TypeScript/JavaScript, Bun/Deno, Dart/Flutter, and Gleam implementations.
