# ORESoftware CI continuity project delivery — August 5, 2026

## Project routing

- GitHub owner: [`ORESoftware`](https://github.com/ORESoftware)
- GitHub Project: [ORESoftware Project #1](https://github.com/orgs/ORESoftware/projects/1)
- Canonical implementation repository: [`ORESoftware/k8s-cluster`](https://github.com/ORESoftware/k8s-cluster)
- Linear project: [`github.com/ORESoftware/k8s-cluster`](https://linear.app/denman/project/githubcomoresoftwarek8s-cluster-c9e32add54f1)
- Linear status: [CI continuity execution status — August 5, 2026](https://linear.app/denman/document/ci-continuity-execution-status-august-5-2026-7e2606e25d32)
- Primary Linear issues: DEN-1549, DEN-1550, DEN-1597, DEN-1606

Shared Kubernetes, official Actions Runner Controller, bounded workflow planning, pre-submit executor routing, fixed-profile execution, and multi-provider activation belong on this Project and Linear project. Queue/Raft/fencing authority belongs to the `fiducia-cloud` board. Standalone source and extraction provenance belong to the `gha-indie-worker` board.

## Architecture boundary

GitHub-hosted runners and official ARC provide native GitHub Actions semantics. The independent Rust path is complementary and deliberately bounded:

1. `gha-clone-server-rs` accepts reviewed repositories, immutable revisions, direct workflow paths, a bounded YAML subset, and fixed build profiles.
2. `gha-executor-router` selects one reviewed provider before submission and pins status to that provider.
3. `dd-build-server` executes operator-reviewed fixed profiles and retains bounded build/log/artifact behavior.
4. `gha-capacity-broker-rs` classifies hosted/ARC capacity policy but never executes repository commands.
5. Fiducia provides the future durable ownership and fencing boundary for multi-replica operation.

The independent lane does not claim full GitHub Actions parity. Unsupported matrices, dynamic expressions, arbitrary actions, caller-selected shell or image, environments, OIDC, deployments, signing, and platform-native jobs remain native-only or fail closed.

## Final merge ledger

| Capability | Pull request | Merge commit |
|---|---:|---|
| Atomic direct and webhook-batch run admission | [`k8s-cluster#751`](https://github.com/ORESoftware/k8s-cluster/pull/751) | `a14072064f25d7b49807656d4231f93d335a6d55` |
| Semantic transport, origin, runtime-bound, and build-identity union | [`#764`](https://github.com/ORESoftware/k8s-cluster/pull/764) | `b827d1fde69bdfc5acfeb9d8a785f184c3ce5505` |
| Live-process redirect, poll-before-trust, identity, and zero-bound tests | [`#843`](https://github.com/ORESoftware/k8s-cluster/pull/843) | `fee1b96e90cd340fb65da26fd4c785a8bb1eeb1c` |
| Raw exact-profile policy byte hardening | [`#844`](https://github.com/ORESoftware/k8s-cluster/pull/844) | `a9776dce110a348c531dcab22244847c3e419184` |
| Canonical portfolio project-link registry and daily reconciler | [`#877`](https://github.com/ORESoftware/k8s-cluster/pull/877) | `74bd901418c61bfe48a5e0480b2d577564100179` |
| Cross-organization delivery ledger | [`#973`](https://github.com/ORESoftware/k8s-cluster/pull/973) | `c612ba91efc10c98c8de9856b89459e61e776e1c` |

## Safety properties now covered

- Direct requests reserve run capacity before task creation.
- Webhook batches reserve all runs or none.
- Active work is never evicted to make room.
- Failed webhook admission releases the delivery claim.
- Build-server redirects are disabled.
- Build-server configuration is a reviewed credential-free origin.
- Accepted build IDs are bounded, path-safe, and bound through every poll.
- Rejected or untrusted submission identities cause zero polling side effects.
- Planner, polling, execution, retention, delivery-TTL, and delivery-capacity bounds reject zero before the process binds.
- Exact repository/profile policy size is measured against the original UTF-8 bytes before whitespace normalization.
- Empty, malformed, or duplicate compiled profile entries fail closed.

## AWS/Hetzner no-duplicate rule

Provider choice may change only before the first `POST /builds` attempt. After submission starts, timeout, reset, redirect, 429, 5xx, malformed acceptance, or polling failure remains pinned to that provider and must not produce a second provider submission.

Keep the clone server and executor router at one active replica until request assignment, webhook delivery claims, executor job/artifact identity, and ownership are durable and Fiducia-fenced.

## Project/document reconciliation

The canonical registry and validation/reconciliation workflows are checked into `ORESoftware/k8s-cluster`. Organization-specific GitHub and Linear delivery records have been published for ORESoftware, Fiducia, and gha-indie-worker.

Provider-wide GitHub Projects v2 mutation remains protected by a separate project-write credential. A one-time encrypted bridge failed safely because `PROJECT_SYNC_GITHUB_TOKEN` was not configured; no plaintext token was available, printed, or committed. The registry, validation, repository documentation, PRs, and Linear records are current; fleet-wide provider apply remains gated on provisioning the reviewed least-privilege credential.

## Remaining activation gates

1. Provision separate least-privilege identities for Actions billing read, ARC registration, private workflow/source read, and selected-repository capacity mutation.
2. Publish signed, scanned, SBOM/provenance-attested immutable runner and executor images.
3. Register official ARC scale sets in AWS and Hetzner with zero warm runners and bounded maxima.
4. Run exact-SHA native ARC smoke jobs on both providers.
5. Prove provider-loss, cancellation, cleanup, artifact, and rollback behavior.
6. Implement durable assignment and delivery ownership with Fiducia fencing before horizontal scaling.
7. Obtain an independent write-access approval for `gha-indie-worker/gha-clone-server.rs#2`; squash auto-merge is already enabled.