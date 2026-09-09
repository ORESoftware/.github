# MCP real-TJSV execution checkpoint — 2026-09-09

Tracking: DEN-970, DEN-957, DEN-3828, and `ORESoftware/typespec-json-schema-validator#20`.

This is an execution checkpoint for the MCP contract runner, not another TJSV roadmap. The broader language-boundary and runtime-validation roadmaps remain authoritative for fleet sequencing. This note records the concrete `ORESoftware/mcp-rust-libs` implementation slice and its promotion gate.

## Published implementation

Carrier PR: https://github.com/ORESoftware/mcp-rust-libs/pull/41

The PR pins `ORESoftware/typespec-json-schema-validator` to immutable revision `4740f1367a7906813dcd420a77d0c9ede26943fb` and changes the consuming repository's hosted contract workflow so it no longer relies only on validator doubles.

The proposed exact-head workflow now:

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
11. calls the pinned TJSV language/runtime-boundary verifier and requires fail-closed behavior when evidence is incomplete.

The consuming repository also records the immutable validator pin in `tooling/org-mcp-contract/tjsv.lock.json`, adds governed `tmp/` and `temp/` ignores, and documents the promotion sequence in `docs/tjsv-runtime-boundary-gate.md`.

## Authority invariant

Human-authored TypeSpec and independently human-authored JSON Schema/OpenAPI remain peer top-level authorities. Generated JSON Schema, Contract IR, generated clients, runtime adapters, Protobuf/WIT/SQL/ORM projections, manifests, and verification receipts are evidence only. A generated artifact cannot overwrite an authored authority or resolve disagreement by precedence.

Runtime/language promotion must bind evidence to the exact parity receipt, Contract IR, immutable source revision, artifact digest, generator, and native toolchain. Missing, stale, unsupported, mismatched, skipped, or non-passed required evidence is not success.

## Regular versus administrator MCP boundary

Contract parity does not collapse the planned regular/admin MCP split. Fleet repositories should keep ordinary `*-mcp-server.rs` and privileged `*-admin-mcp-server.rs` services as separate deployable and permission boundaries where administrator commands exist.

Shared `*-interfaces`, `*-lib-core`, and `*-orm-core` contracts may be reused, but the two service families retain separate repository permissions, binaries, workload/service identities, credentials, OAuth audiences, network/VPC boundaries, release approvals, and authorization policy. Client-supplied `role`, `is_admin`, tenant, or similar fields never establish authority.

Read/query MCP tools and administrator command tools also need different operational guarantees. Administrator commands require action-level authorization, tenant/resource checks, idempotency/replay protection, concurrency control, locks/fencing where applicable, and audited approval for destructive or financial operations. TJSV proves representation/validation convergence; it is not an authorization system.

## Exact-head merge gate

The `mcp-rust-libs` PR must remain unmerged until every applicable hosted check for its exact proposed head is terminal and green, the branch is reconciled with current `main` without rebase/history rewriting, and GitHub reports it mergeable with no review/ruleset blocker.

After merge, DEN-970 should record the merge commit and post-merge workflow evidence. Fleet consumers should then adopt the reviewed runner/TJSV revisions through their own exact-head PRs rather than copying a green status literal or following a moving branch.

## Credential boundary

No GitHub, Linear, cloud, database, or other credential belongs in this public checkpoint, repository fixtures, workflow arguments, contract manifests, diagnostics, or receipts. Connected authenticated tooling or approved secret stores provide access; transcript-pasted credentials are not a dependency mechanism.
