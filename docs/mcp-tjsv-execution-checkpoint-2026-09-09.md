# MCP real-TJSV execution checkpoint — 2026-09-09

Tracking: DEN-970, DEN-957, DEN-3828, DEN-3830, and `ORESoftware/typespec-json-schema-validator#20`.

This is an execution checkpoint for the MCP contract runner, not another TJSV roadmap. The broader language-boundary and runtime-validation roadmaps remain authoritative for fleet sequencing. This note records the concrete `ORESoftware/mcp-rust-libs` implementation slice, the failures found by hosted execution, their repairs, the final merge evidence, and the bounded fleet tasks created from that evidence.

## Merged implementation and exact evidence

Carrier PR: https://github.com/ORESoftware/mcp-rust-libs/pull/41

PR #41 passed every applicable exact-head workflow at `e23bbebb94e1c5180e1e28c25642a0f3b2bcf8d4` and was merged with a normal merge as `ed98a3ce98d46e6e0c80b03c5e57e50d4bb75ee2`.

The merge commit's `main` push then independently passed:

- Organization MCP contract runner, run `34393052088`;
- repository CI, run `34393052103`;
- Zed MCP dependency contract, run `34393052102`.

The Organization MCP contract runner on the merge commit passed all of these stages:

1. dependency-free MCP runner and exact-catalog regressions;
2. checkout of the reviewed immutable TJSV commit with checkout credentials disabled;
3. TJSV production dependency audit;
4. the exact supported locked install via plain `npm ci`;
5. the pinned TJSV full `test:all` repository gate;
6. TJSV `release:preflight` package-boundary and clean-consumer acceptance;
7. real compiler-backed TypeSpec versus independently authored JSON Schema Draft 2020-12 admission;
8. current Contract IR build/re-verification against the exact authored inputs;
9. accepted/rejected runtime values in both independent schema lanes;
10. non-mutation of both authored authorities;
11. fail-closed intentional peer-authority disagreement and post-admission source drift;
12. the pinned TJSV language/runtime-boundary verifier with fail-closed incomplete-evidence behavior.

The merged runner also supports exact tool-catalog admission so a regular MCP binary cannot remain green while advertising an undeclared additional tool.

## Upstream merge-result regression and repair

The first real hosted consumer execution stopped before compiler-backed consumer integration because its immutable TJSV pin, `4740f1367a7906813dcd420a77d0c9ede26943fb`, failed the validator's own unit gate.

That failure exposed a semantic merge-integration regression, not a reason to weaken the verifier. TJSV PR #76 had been green on its feature head, but `main` advanced concurrently with stricter DEN-3830 language-boundary admission. The merged Lambda unit witness lacked the newly required explicit findings inventory, differential coverage/probe/refusal evidence, and complete Contract IR scope inventory.

Repair PR https://github.com/ORESoftware/typespec-json-schema-validator/pull/84 updated only the stale test witness and added fail-closed negative controls for incomplete differential evidence, incomplete Contract IR scope, and retained parity findings. It passed the full Ubuntu/macOS exact-head gates and merged as `6d560db590cd1a9e03822697f91f6a3f78f6c22a`. That exact merge commit then passed TJSV `main` push CI on both platforms.

`mcp-rust-libs` therefore pins `6d560db590cd1a9e03822697f91f6a3f78f6c22a`. Immutability is required, but an immutable red upstream commit is not promotable merely because a different feature head was green.

Organization-wide safe upgrade automation owns this rule in https://github.com/ORESoftware/.github/issues/55: distinguish `pr_head_green` from `merge_commit_green`, and require terminal upstream evidence for the exact commit a consumer will actually pin.

## Consumer install-policy regression

The next consumer run used the repaired upstream-green TJSV commit but still stopped because the MCP workflow installed it with `npm ci --ignore-scripts`. The exact locked TJSV dependency closure contains `@oresoftware/f2e`, whose package declares an install lifecycle. TJSV's own reviewed CI uses plain `npm ci`.

Commit identity plus lockfile identity therefore did not guarantee execution equivalence: the consumer wrapper had changed dependency build behavior.

The MCP gate was corrected to mirror the reviewed upstream lifecycle, then strengthened to run the TJSV production audit, full repository gate, and release preflight before downstream contract integration. The exact-head and merge-result runs passed under that profile.

`.github#55` now also owns consumer execution-equivalence policy: package manager/version, install profile, lifecycle policy, lock digest, registry/toolchain identity, and build prerequisites are evidence when they can change the executable dependency closure. This does **not** mean blindly enabling arbitrary lifecycle scripts; alternate hardened profiles require their own exact reviewed evidence.

## Authority invariant

Human-authored TypeSpec and independently human-authored JSON Schema/OpenAPI remain peer top-level authorities. Generated JSON Schema, Contract IR, generated clients, runtime adapters, Protobuf/WIT/SQL/ORM projections, manifests, and verification receipts are evidence only. A generated artifact cannot overwrite an authored authority or resolve disagreement by precedence.

Runtime/language promotion must bind evidence to the exact parity receipt, Contract IR, immutable source revision, artifact digest, generator, and native toolchain. Missing, stale, unsupported, mismatched, skipped, zero-step, or non-passed required evidence is not success.

## Exact regular/admin MCP catalog boundary

The merged runner supports an explicit closed-catalog promotion profile:

- `coverage: "exact-tools"` requires `serverClass: "regular"` or `"admin"`;
- each declared operation carries reviewed `surface: "regular"` or `"admin"` metadata;
- a regular manifest cannot declare an admin-surface tool;
- `tools/list` must equal the reviewed manifest exactly, so any undeclared extra tool fails promotion;
- legacy `coverage: "declared-tools-only"` remains explicitly partial during migration and does not certify undeclared tools.

The negative suite includes the critical case where every expected regular tool is present but the binary also advertises one undeclared admin-looking tool. Presence of all expected tools is not sufficient for exact certification.

This is stronger than an `admin_` name-prefix convention, but `surface` remains evidence/review metadata rather than authentication. Fleet repositories should keep ordinary `*-mcp-server.rs` and privileged `*-admin-mcp-server.rs` services as separate deployable and permission boundaries where administrator commands exist.

Shared `*-interfaces`, `*-lib-core`, and `*-orm-core` contracts may be reused, but the two service families retain separate repository permissions, binaries, workload/service identities, credentials, OAuth audiences, network/VPC boundaries, release approvals, and authorization policy. Client-supplied `role`, `is_admin`, tenant, or similar fields never establish authority.

Read/query MCP tools and administrator command tools also need different operational guarantees. Administrator commands require action-level authorization, tenant/resource checks, idempotency/replay protection, concurrency control, locks/fencing where applicable, and audited approval for destructive or financial operations. TJSV proves representation/validation convergence; it is not an authorization system.

Fleet rollout of exact catalog admission is tracked in https://github.com/ORESoftware/.github/issues/178. Its acceptance includes at least 12 regular real-binary consumers plus at least one separately deployed administrator MCP service proving regular-to-admin credential denial.

## Promotion after this checkpoint

`ed98a3ce98d46e6e0c80b03c5e57e50d4bb75ee2` is the first merged `mcp-rust-libs` revision from this execution slice with both exact-head and post-merge green evidence.

Fleet consumers should adopt the reviewed runner/TJSV revisions through their own DEN-linked exact-head PRs rather than copying a green status literal or following a moving branch. Multi-repository rollout must continue to honor the compatibility, lock-consistency, and cohort-admission work already tracked in `.github#75`, `#77`, and `#136`.

## Credential boundary

No GitHub, Linear, cloud, database, or other credential belongs in this public checkpoint, repository fixtures, workflow arguments, contract manifests, diagnostics, or receipts. Connected authenticated tooling or approved secret stores provide access; transcript-pasted credentials are not a dependency mechanism. No credential was revoked or rotated as part of this work.
