# Lambda OCI + TJSV fleet rollout

Linear: `DEN-3959`

GitHub tracker: `ORESoftware/.github#69`

This document defines the public-safe organization-level rollout contract for repositories matching `*-lambdas`. Detailed private-repository assignments, authenticated inventory, and access blockers live in Linear and other approved private systems; this file intentionally does not publish private repository names or credentials.

## Goals

Every participating Lambda repository should have a provider-neutral core, thin provider adapters, reproducible artifacts, explicit Docker/OCI behavior, and independently authored TypeSpec and JSON Schema Draft 2020-12 authorities whose convergence is enforced by `ORESoftware/typespec-json-schema-validator` (TJSV).

The rollout must not collapse TypeSpec and JSON Schema into one source of truth. Generated schemas, generated clients, Contract IR, and runtime receipts are evidence only.

## Required contract model

Maintain two independent authored lanes:

```text
TypeSpec -> protocol/persistence/runtime projections
JSON Schema/OpenAPI -> interfaces/types/validators/HTTP/write projections
```

TJSV compares the authored authorities and their evidence. Consumers pin TJSV to an immutable reviewed commit SHA. Mutable branches or tags are not sufficient for a release gate.

Any unexplained authority mismatch is fail-closed and blocks release, merge, deployment, or provider promotion.

## Container and OCI baseline

Where the provider/runtime supports containers:

- build and test `linux/amd64` and `linux/arm64`;
- use multi-stage Dockerfile/Containerfile builds;
- retain source revision and target architecture provenance;
- keep the runtime image minimal and non-root where practical;
- produce OCI-compatible output and a combined OCI layout/index where supported;
- test the packaged artifact itself rather than only source-tree execution.

`entrypoint.sh` remains the generic OCI process contract. It must:

- preserve command arguments through `"$@"`;
- never reconstruct untrusted commands with `eval`;
- avoid reflecting secret-bearing argv in logs;
- preserve the workload's exact nonzero exit status;
- forward termination signals;
- reap/terminate helper children cleanly;
- support combined stdout/stderr ingestion or separate stream processors;
- define explicit fail-open/fail-closed helper behavior;
- avoid recursive helper logging loops;
- bound shutdown/draining behavior rather than hanging indefinitely.

Managed serverless runtimes that cannot host a long-lived helper process should use equivalent in-process or provider-native telemetry instead of pretending the OCI process model applies.

## Provider adapter baseline

Keep domain logic provider-neutral. Adapters should remain thin and separately testable for the providers a repository actually supports, including as applicable:

- AWS Lambda;
- Google Cloud/Cloud Run;
- Azure Functions or container-based Azure targets;
- Vercel Functions;
- generic OCI/Kubernetes/container execution.

Use shared positive/negative fixtures across adapters so behavior drift is visible. Unsupported combinations should be explicit and tested as unsupported rather than silently skipped.

## Cross-runtime evidence

For contracts that cross language/runtime boundaries, add native witnesses for the runtimes actually supported by the repository. Rust, TypeScript, and Dart/Flutter are the minimum common internal targets where applicable.

Each runtime witness should exercise:

- required/optional/null behavior;
- enum and union wire values;
- field names and unknown-field behavior;
- scalar widths/formats and boundary values;
- serialization/read-back;
- malformed and out-of-range rejection;
- provider request/response/error envelopes.

Missing runtime evidence is `partial`, not inferred success.

## JavaScript / TypeScript artifact policy

When Node.js handlers exist, bundle each deployable handler to one JavaScript artifact where practical and test that artifact without access to the source checkout or development `node_modules`.

Bun and Deno standalone executables may be additional target-specific artifacts when the intended provider/runtime accepts them. They must be tested per OS/architecture and must not be treated as interchangeable with managed Node runtimes without provider-level evidence.

## Follow-up work classes

The detailed assignments are tracked privately under DEN-3959. The public-safe work queue is:

1. Restore Actions runner admission wherever jobs terminate before executing any step, without weakening TJSV/Rust/OCI gates. See #125.
2. Repair sibling test-organization read boundaries so exact private source SHAs can be certified through approved secret channels. See #126.
3. Salvage unique tests/contracts/docs from stale Lambda portability PRs after semantic comparison with current `main`; preserve originals unless explicitly authorized to close them. See #148.
4. Re-evaluate stale dependency-sync PRs against current manifests, lockfiles, dependency versions, and current `main`. See #152.
5. Bootstrap empty Lambda repositories from the verified canonical template, replacing placeholders with real domain contracts before claiming support. See #152.
6. Audit repositories whose default branch is a feature/portability branch and normalize only through an explicit reviewed change. See #152.
7. Roll the verified baseline through successive consumer tranches while preserving each repository's provider-specific behavior and domain authority.
8. Add Rust + TypeScript + Dart/Flutter runtime witnesses where those runtimes are supported. See #131.
9. Add provider adapter smoke fixtures across supported cloud/serverless targets. See #134.
10. Add packaged-artifact tests for Node bundles and optional Bun/Deno standalone targets where relevant. See #145.
11. Evaluate a reusable Rust process supervisor for PID 1, child reaping, signal forwarding, and stdout/stderr helper semantics while retaining `entrypoint.sh` as the OCI contract surface. See #144.
12. Maintain a private machine-readable fleet receipt with per-repository rollout evidence and blockers. See #128.

## Current execution snapshot — 2026-09-09

Verified merged tranches now include the canonical template plus multiple real Lambda consumers. The canonical template has post-merge green evidence for TJSV, Rust tests/Clippy, entrypoint tests, `linux/amd64` and `linux/arm64` image builds, AWS artifacts, and combined OCI layout generation. The next-wave work is no longer a single undifferentiated fleet task; it is decomposed into executable child issues:

- #125 — restore Lambda Actions runner admission;
- #126 — repair exact-private-SHA sibling certification;
- #128 — build the deterministic machine-readable fleet receipt;
- #131 — add Rust/TypeScript/Dart runtime witnesses;
- #134 — add the cross-provider adapter smoke matrix;
- #144 — evaluate the reusable Rust process supervisor;
- #145 — add packaged Node/Bun/Deno artifact tests;
- #148 — semantically salvage unique work from stale Lambda portability branches onto current `main`;
- #152 — inventory bootstrap-only repositories, unexpected default branches, and stale dependency-sync work before any mutation.

Two failure classes must remain distinct in evidence:

1. **runner/admission blocked** — no hosted job step executes, so this is not a failed TJSV or runtime assertion;
2. **private-source read blocked** — the test runner executes but the approved read-only credential cannot fetch the exact production source SHA.

Neither class may be relabeled as code success or bypassed with mutable refs, copied private source, transcript credentials, or weakened required checks.

## Stale-work salvage and fleet hygiene

Stale portability work is a provenance source, not a merge strategy. For each stale PR, classify every changed path as `identical_on_main`, `semantically_integrated`, `superseded`, `unique_safe`, `unique_conflicting`, or `requires_owner_decision`; inspect the merge base, current replacement, relevant history, and linked contract/runtime work before acting. Fresh salvage starts from current `main`. Cherry-pick an old commit only when the whole commit is still conceptually valid and conflict-free; otherwise reconstruct the useful intent in focused new commits. Keep the historical PR open unless a human explicitly authorizes closure.

Bootstrap/default-branch/dependency discovery is read-only. Do not silently change default branches, delete branches, close dependency PRs, or scaffold an empty repository as a side effect of inventory. Before adopting the canonical template, replace placeholders with real domain contracts and preserve repository-specific provider/runtime behavior. Re-evaluate stale dependency updates against current manifests, locks, advisory context, and current `main`.

## Canonical public baseline

`ORESoftware/ores-lambdas-template` is the reusable scaffold. Its `main` branch must remain green for:

- TJSV peer-authority convergence;
- Rust tests and warnings-denied Clippy;
- entrypoint contract tests;
- `linux/amd64` and `linux/arm64` container builds;
- combined OCI layout generation;
- provider-specific artifact jobs configured by the template.

`ORESoftware/typespec-json-schema-validator` is the convergence/admission implementation. Consumer repositories use reviewed immutable pins and retain evidence artifacts.

The shared Lambda cross-runtime regression profile is represented by the merged TJSV work in `ORESoftware/typespec-json-schema-validator#76`. This does not authorize blind fleet repinning. Pin/channel compatibility and repository-local consumer-lock consistency are separate reviewed gates tracked in #75 and #77; an older immutable pin is neither silently promoted nor silently invalidated without fresh compatibility and exact-head evidence.

## Completion evidence

A rollout item is complete only when authoritative remote evidence exists:

- pushed commit(s);
- pull request URL;
- exact-head or post-merge CI result for all required gates;
- merge SHA where merged;
- updated private fleet receipt / Linear task status.

Local tests alone are not completion evidence.

## Security and Git safety

Never place credentials, private repository inventories, private source archives, customer data, or decrypted environment values in this public repository.

Follow `agents.md` for semantic conflict resolution and non-destructive Git policy. In particular, do not use rebase, reset, stash, force-push, blanket ours/theirs conflict resolution, or policy/check bypasses to make rollout work appear green.
