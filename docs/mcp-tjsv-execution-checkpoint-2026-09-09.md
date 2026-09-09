# MCP real-TJSV execution checkpoint — 2026-09-09

Tracking: DEN-970, DEN-957, DEN-3828, DEN-3830, and `ORESoftware/typespec-json-schema-validator#20`.

This is an execution checkpoint for the MCP contract runner, not another TJSV roadmap. The broader language-boundary and runtime-validation roadmaps remain authoritative for fleet sequencing. This note records the concrete `ORESoftware/mcp-rust-libs` implementation slice, the merge-result regression discovered while testing it, and the promotion/fleet tasks created from that evidence.

## Published implementation

Carrier PR: https://github.com/ORESoftware/mcp-rust-libs/pull/41

The PR consumes `ORESoftware/typespec-json-schema-validator` by reviewed immutable commit and changes the consuming repository's hosted contract workflow so it no longer relies only on validator doubles.

The exact-head workflow now:

1. runs the dependency-free MCP runner regression suite;
2. checks out the exact reviewed TJSV commit with checkout credentials disabled;
3. installs the validator's locked npm graph;
4. runs the pinned TJSV unit suite;
5. executes real compiler-backed TypeSpec versus independently authored JSON Schema Draft 2020-12 admission;
6. builds and re-verifies Contract IR against current source inputs;
7. checks accepted and rejected runtime values in both independent schema lanes;
8. proves neither authored authority is rewritten;
9. proves an intentional peer-authority disagreement stops admission;
10. proves post-admission source drift invalidates retained evidence;
11. calls the pinned TJSV language/runtime-boundary verifier and requires fail-closed behavior when evidence is incomplete;
12. exercises exact tool-catalog admission so a regular MCP binary cannot stay green while advertising an undeclared extra tool.

The consuming repository also records the immutable validator pin in `tooling/org-mcp-contract/tjsv.lock.json`, adds governed `tmp/` and `temp/` ignores, and documents the promotion sequence in `docs/tjsv-runtime-boundary-gate.md`.

## Upstream merge-result regression and repair

The first real hosted consumer execution intentionally stopped before compiler-backed consumer integration because its immutable TJSV pin, `4740f1367a7906813dcd420a77d0c9ede26943fb`, failed the validator's own `npm test` gate.

That failure exposed a semantic merge-integration regression, not a reason to weaken the verifier. TJSV PR #76 had been green on its feature head, but `main` advanced concurrently with stricter DEN-3830 language-boundary admission. The merged Lambda unit witness lacked the newly required explicit findings inventory, differential coverage/probe/refusal evidence, and complete Contract IR scope inventory.

Repair PR https://github.com/ORESoftware/typespec-json-schema-validator/pull/84 updated only the stale test witness and added fail-closed negative controls for incomplete differential evidence, incomplete Contract IR scope, and retained parity findings. It passed the full Ubuntu/macOS exact-head gates and merged as `6d560db590cd1a9e03822697f91f6a3f78f6c22a`. That exact merge commit then passed the TJSV `main` push CI on both platforms.

`mcp-rust-libs#41` is therefore repinned to `6d560db590cd1a9e03822697f91f6a3f78f6c22a`. Immutability remains required, but an immutable red upstream commit is not promotable merely because its feature head was green.

Organization-wide safe upgrade automation owns this newly proven rule in https://github.com/ORESoftware/.github/issues/55: distinguish `pr_head_green` from `merge_commit_green`, and require the exact upstream commit a consumer will pin to have terminal green upstream evidence.

## Authority invariant

Human-authored TypeSpec and independently human-authored JSON Schema/OpenAPI remain peer top-level authorities. Generated JSON Schema, Contract IR, generated clients, runtime adapters, Protobuf/WIT/SQL/ORM projections, manifests, and verification receipts are evidence only. A generated artifact cannot overwrite an authored authority or resolve disagreement by precedence.

Runtime/language promotion must bind evidence to the exact parity receipt, Contract IR, immutable source revision, artifact digest, generator, and native toolchain. Missing, stale, unsupported, mismatched, skipped, zero-step, or non-passed required evidence is not success.

## Exact regular/admin MCP catalog boundary

The runner now supports an explicit closed-catalog promotion profile:

- `coverage: "exact-tools"` requires `serverClass: "regular"` or `"admin"`;
- each declared operation carries reviewed `surface: "regular"` or `"admin"` metadata;
- a regular manifest cannot declare an admin-surface tool;
- `tools/list` must equal the reviewed manifest exactly, so any undeclared extra tool fails promotion;
- legacy `coverage: "declared-tools-only"` remains explicitly partial during migration and does not certify undeclared tools.

This is stronger than relying on an `admin_` name prefix, but it is still evidence/review metadata rather than authentication. Fleet repositories should keep ordinary `*-mcp-server.rs` and privileged `*-admin-mcp-server.rs` services as separate deployable and permission boundaries where administrator commands exist.

Shared `*-interfaces`, `*-lib-core`, and `*-orm-core` contracts may be reused, but the two service families retain separate repository permissions, binaries, workload/service identities, credentials, OAuth audiences, network/VPC boundaries, release approvals, and authorization policy. Client-supplied `role`, `is_admin`, tenant, or similar fields never establish authority.

Read/query MCP tools and administrator command tools also need different operational guarantees. Administrator commands require action-level authorization, tenant/resource checks, idempotency/replay protection, concurrency control, locks/fencing where applicable, and audited approval for destructive or financial operations. TJSV proves representation/validation convergence; it is not an authorization system.

Fleet rollout of exact catalog admission is a new bounded task: https://github.com/ORESoftware/.github/issues/178. Its acceptance includes at least 12 regular real-binary consumers plus at least one separately deployed administrator MCP service proving regular-to-admin credential denial.

## Exact-head merge gate

The `mcp-rust-libs` PR must remain unmerged until every applicable hosted check for its exact proposed head is terminal and green, the branch is reconciled with current `main` without rebase/history rewriting, and GitHub reports it mergeable with no review/ruleset blocker.

After merge, DEN-970 should record the merge commit and post-merge workflow evidence. Fleet consumers should then adopt the reviewed runner/TJSV revisions through their own exact-head PRs rather than copying a green status literal or following a moving branch.

## Credential boundary

No GitHub, Linear, cloud, database, or other credential belongs in this public checkpoint, repository fixtures, workflow arguments, contract manifests, diagnostics, or receipts. Connected authenticated tooling or approved secret stores provide access; transcript-pasted credentials are not a dependency mechanism. No credential was revoked or rotated as part of this work.
