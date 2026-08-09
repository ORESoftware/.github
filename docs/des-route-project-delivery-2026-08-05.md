# Canonical `/des` route delivery and project routing

**Delivery date:** August 5, 2026  
**Application owner:** [`discrete-event-systems`](https://github.com/discrete-event-systems)  
**GitOps owner:** [`ORESoftware/k8s-cluster`](https://github.com/ORESoftware/k8s-cluster)

## Planning and Project routing

The canonical product board is [`discrete-event-systems-project`](https://github.com/orgs/discrete-event-systems/projects/1). The paired planning project is [`github.com/discrete-event-systems`](https://linear.app/denman/project/githubcomdiscrete-event-systems-4a3086ae0c45).

Organization routing documentation is published in [`discrete-event-systems/.github/PROJECTS.md`](https://github.com/discrete-event-systems/.github/blob/main/PROJECTS.md). Fleet-wide GitHub Project and Linear reconciliation is controlled by [Linear DEN-2242](https://linear.app/denman/issue/DEN-2242/reconcile-github-projects-and-linear-documentation-across).

`ORESoftware` is the owner account for the shared GitOps repository; the product work is routed to the `discrete-event-systems` organization Project, while cluster execution is tracked in repository issue [`k8s-cluster#991`](https://github.com/ORESoftware/k8s-cluster/issues/991) and the repository-specific Linear project [`github.com/ORESoftware/k8s-cluster`](https://linear.app/denman/project/githubcomoresoftwarek8s-cluster-c9e32add54f1).

The latest fleet Project reconciliation evidence was affected by GitHub API rate limiting. Therefore, the board URL is the canonical routing target, but project-item attachment must not be claimed until DEN-2242 publishes a successful rate-aware result. The repository issues and Linear records below remain authoritative during that verification window.

## Delivered implementation

### Application

- PR: [`discrete-event-systems/des-web.rs#10`](https://github.com/discrete-event-systems/des-web.rs/pull/10)
- final source head: `77741ec8b5331617f71416748ef5f06846e43a5d`
- merge commit: `e7d8b284dd796826bc09120bbd10295b0bf2783f`
- documentation PRs: [`#13`](https://github.com/discrete-event-systems/des-web.rs/pull/13) and [`#14`](https://github.com/discrete-event-systems/des-web.rs/pull/14)
- final documentation merge: `360ddfd4a51dd2ecdd555c778e161985411ca16c`

### GitOps

- implementation PR: [`ORESoftware/k8s-cluster#872`](https://github.com/ORESoftware/k8s-cluster/pull/872)
- final source head: `16b9ecbad319a5433f5a58dec6e386ea48605f05`
- merge commit: `7b77b48dcb347a0c474da1831e09f27338db43c1`
- delivery/rollout documentation PR: [`#996`](https://github.com/ORESoftware/k8s-cluster/pull/996)
- documentation merge: `24e40c65b19d3673c7f5512aa76f9e82e082c430`

### Immutable artifact

```text
ghcr.io/discrete-event-systems/des-web.rs:sha-77741ec8b5331617f71416748ef5f06846e43a5d@sha256:c3b32a5ef767bcdba515c8199fce363871ba2916e4c824609a09a37b3adc02e5
```

The image was published from the same source revision that passed application CI, with provenance and an SBOM, and is pinned by both SHA tag and digest in GitOps.

## Architecture and ownership

```text
browser /des/*
  -> dd-remote-gateway
  -> dd-des-simulator Service :8099 (compatibility name)
  -> selector app=dd-des-web
  -> dd-des-web pod :8130
  -> dd-des-rs :8112 for engine solve/stream work
  -> private Postgres only for optional persisted state
```

- `discrete-event-systems/des-web.rs` owns pages, route taxonomy, htmx/browser behavior, API shape, application tests, route documentation, and image publication.
- `ORESoftware/k8s-cluster` owns Deployments, Services, PDB, NetworkPolicy, gateway compatibility, Argo CD, public rollout evidence, and rollback.
- `/des-rs/*` and `/out/*` remain compatibility surfaces; `/des/music` remains an explicit temporary exception.

## Catalog verification

The older GitOps PR merge-reference catalog job reported drift. Current `k8s-cluster/main` was regenerated through the repository's locked Nix toolchain. The generator wrote 86 application records from 121 tracked documents and produced no diff: `catalog/applications.json is already current`.

Evidence: [`Actions run 31035794438`](https://github.com/ORESoftware/k8s-cluster/actions/runs/31035794438)

## Authoritative trackers

- DES GitHub tracker: [`discrete-event-systems/des-web.rs#11`](https://github.com/discrete-event-systems/des-web.rs/issues/11)
- GitOps rollout tracker: [`ORESoftware/k8s-cluster#991`](https://github.com/ORESoftware/k8s-cluster/issues/991)
- Completed implementation issue: [`DEN-1936`](https://linear.app/denman/issue/DEN-1936/des-webrsk8s-cluster-consolidate-public-des-pages-under-des)
- Active rollout issue: [`DEN-2280`](https://linear.app/denman/issue/DEN-2280/k8s-clusterdes-webrs-verify-the-canonical-des-rollout-in-aws-and)
- Architecture document: [DES route consolidation and GitOps ownership](https://linear.app/denman/document/des-route-consolidation-and-gitops-ownership-dc64657c976f)

## Remaining operational gates

1. Sync `dd-next-runtime` in both AWS and Hetzner Argo CD control planes.
2. Verify the canonical pages, catalog API, health/readiness probes, engine delegation, database-backed fragments, and degraded no-database mode through both public entry points.
3. Record compatibility request counts for `/des-rs/*`, `/out/*`, and `/des/music` before removal.
4. Record rollback evidence, or a successful no-rollback conclusion, in GitHub and Linear.

## Independent CI authentication issue

Repository-wide jobs still have a private `remote/libs` checkout defect that is independent of the focused DES route contract and rendered manifests. The repair is tracked in [`ORESoftware/k8s-cluster#997`](https://github.com/ORESoftware/k8s-cluster/issues/997) and [Linear DEN-2284](https://linear.app/denman/issue/DEN-2284/k8s-ci-rotate-the-dedicated-remotelibs-deploy-key-and-restore-required).

## Rollback

Restore the `dd-des-simulator` Service selector to `app: dd-des-simulator`, scale the legacy simulator Deployment above zero, sync `dd-next-runtime`, and verify `/des/`. The public URL remains unchanged.
