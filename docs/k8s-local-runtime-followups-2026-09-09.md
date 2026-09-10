# k8s-cluster local-runtime and namespace follow-up roadmap — 2026-09-09

This document records the next reviewed work discovered from exact-head validation of `ORESoftware/k8s-cluster` local Kubernetes, namespace migration, and private-backend CI. It is a coordination document; the implementation authorities remain the linked repositories, pull requests, GitHub issues, and canonical Linear parents.

## Current evidence baseline

### `ORESoftware/k8s-cluster#1540`

Exact reviewed head: `fd9c38752349d5286cd2ab835e80f3c4b65244da`.

The branch has substantive credential-free local Kubernetes evidence in addition to its Daedalus and namespace-repair work:

- kind `v0.30.0` is checksum-pinned;
- the Kubernetes `v1.32.8` node image is digest-pinned;
- pull-request verification checks out the exact PR head rather than relying on the synthetic merge commit;
- every run uses an isolated kubeconfig and evidence directory;
- the namespace classifier, committed inventory, and migration manifest are checked against the exact source tree;
- a disposable Kubernetes API server performs server-side manifest admission;
- the observability exporter identity may list pods but may not read Secrets;
- the dedicated verifier also exercises a two-node topology, Node 22 and Node 24 runtime checks, a hardened Benefactor image build, observability policy, and temporary-file hygiene;
- no AWS or Hetzner provider write is part of the local evidence path.

The uploaded `namespace-kind-smoke-34382598985-1` artifact records 1,366 migration identities, committed/generated inventory equality, zero destructive-cleanup authorizations, `providerWrites=false`, `secretInputs=false`, and RBAC evidence `list-pods=yes` / `get-secrets=no`.

All exact-head workflows are green except `repo checks / backend pins + private deployment contracts`. The narrow `remote/libs` checkout succeeds before that lane fails closed because the repository-level GitHub App secrets were never hydrated.

### `ORESoftware/k8s-cluster#1543`

DEN-1032 already has a separate draft implementation of a reusable local-runtime contract:

- independent human-authored TypeSpec authority;
- independent human-authored JSON Schema Draft 2020-12 peer authority;
- pinned `ORESoftware/typespec-json-schema-validator` parity evidence;
- Colima + kind profile;
- Ubuntu 24.04 Multipass + K3s profile;
- Docker-only negative profile proving a container daemon is not Kubernetes admission;
- fail-closed semantic runtime-profile checks and deterministic evidence.

TypeSpec and authored JSON Schema remain independent top-level authorities. Generated schemas, language bindings, witnesses, and receipts are downstream evidence and are not a third authority.

## External AWS OIDC bootstrap blocker

DEN-1537 is correctly marked complete at the software-contract level: `ORESoftware/k8s-cluster#1546` merged to `main` as `d15aa4c56719edaf929f9308acf0622aa0d2be28` and added bounded trusted-main AWS OIDC role failover for GitHub App bootstrap.

The trusted-main bootstrap then actually executed as Actions run `34370671019`. This resolves the earlier ambiguity about `main` versus `dev`: repository Actions secrets would be visible to trusted PR jobs once hydration succeeds, so forward-porting the bootstrap workflow into `dev` is not the immediate unblocker.

The post-merge run proved the software-side recovery behaved correctly and fail-closed:

- exact trusted-main checkout passed;
- the protected selector self-test passed;
- the exact 32-repository GitHub App allowlist passed;
- `K8S_SUBMODULE_BOOTSTRAP_ROLE_ARN` was not configured, so the dedicated role slot skipped;
- `AWS_ROLE_TO_ASSUME` was configured, but both STS retries failed with `Not authorized to perform sts:AssumeRoleWithWebIdentity`;
- `REMOTE_DEV_AWS_ROLE_TO_ASSUME` was configured and failed with the same STS denial;
- `AWS_OIDC_ROLE_ARN` and `AWS_ECR_ROLE_ARN` were not configured, so those slots skipped;
- the final `Require one approved AWS OIDC role` assertion failed;
- protected SSM secret hydration never ran.

Canonical GitHub recovery tracking remains `ORESoftware/k8s-cluster#886`. The next step is owner-controlled AWS IAM/OIDC remediation:

1. provision `K8S_SUBMODULE_BOOTSTRAP_ROLE_ARN` or correct one approved existing role's web-identity trust for exact subject `repo:ORESoftware/k8s-cluster:ref:refs/heads/main` and audience `sts.amazonaws.com`;
2. retain only the narrowly required SSM authority for the protected administration instance;
3. rerun the trusted-main bootstrap and require one approved role slot to succeed plus repository-secret hydration;
4. verify only the two repository secret names exist, never their values;
5. rerun `k8s-cluster#1540` and require `backend pins + private deployment contracts` to execute the private contracts and pass.

Do not use a PAT fallback, credential-bearing URL, broadened repository allowlist, secret logging, or skipped private checks. A later surgical `main`/`dev` parity port may still be useful because those histories are heavily divergent, but it does not fix repository-level secret hydration.

## New implementation tasks

Linear cannot create additional issues at the moment because the workspace has reached its free issue limit. These GitHub task issues are therefore mapped to existing canonical Linear parents through Linear comments rather than creating duplicate or immediately canceled Linear records.

### 1. `k8s-cluster#1547` — unify local runtime profiles with exact-head kind evidence

Canonical Linear parent: **DEN-1032**. Related migration parent: **DEN-2786**.

Make the RuntimeProfile authorities from `#1543` and the actual kind/API/RBAC evidence from `#1540` one coherent contract. `scripts/ci/local-kind-smoke.sh` should consume or emit a RuntimeProfile-compatible evidence envelope instead of independently duplicating topology, version, and no-cloud-write facts.

Required invariants:

- TypeSpec and authored JSON Schema stay independent peers;
- TJSV checks parity and valid/invalid corpus behavior;
- exact-head checkout remains mandatory;
- kind and node artifacts remain immutable;
- kubeconfig and evidence remain isolated;
- the negative Secret-RBAC assertion remains executable;
- generated receipts/witnesses remain downstream read-only evidence.

This task should land before the architecture-specific local-runtime extensions below so they reuse one contract instead of creating new formats.

### 2. `k8s-cluster#1548` — certify Apple Silicon and amd64 local Kubernetes parity

Canonical Linear parent: **DEN-1032**. Related existing work: **DEN-2584** for Apple Silicon CI runner infrastructure.

Add explicit native architecture contracts for:

- Apple Silicon / arm64 Colima + kind;
- native amd64 Linux/kind;
- Multipass guest architecture;
- OCI workload image platform support.

Cross-architecture x86_64 emulation on Apple Silicon may be useful for compatibility, but it must be marked as emulation and must never be reported as native performance evidence. RuntimeProfile should bind host architecture, guest architecture, emulation mode, and allowed node-image platform, with TJSV drift tests.

### 3. `k8s-cluster#1549` — add a kubeadm/containerd Multipass host-parity tier

Canonical Linear parent: **DEN-1032**.

K3s remains useful for lightweight local clusters, but it must not be used to certify production host behavior when production uses kubeadm/containerd semantics.

Add a clean Ubuntu 24.04 Multipass tier with pinned kubeadm, kubelet, kubectl, containerd, CNI, and host prerequisites. Verify kernel/sysctl assumptions, cgroup/runtime configuration, kubelet startup, API readiness, reboot/rejoin, and service recovery.

Explicitly classify EC2-only behavior as unverified by the local VM, including IMDS, IAM instance profiles, EBS, VPC/security groups, and cloud load-balancer/controller integration. A local VM is host-parity evidence, not proof of those provider surfaces.

### 4. `k8s-cluster#1550` — move DEN-2786 namespace verification from Python toward Rust

Canonical Linear parent: **DEN-2786**.

Move the classifier, deterministic inventory/manifest verification, canonical serialization, and evidence generation toward a small Rust CLI/library. Preserve the exact current 1,366-entry contract before changing callers.

Cutover requirements:

1. inventory all Python entry points and callers;
2. port adversarial behavior first;
3. run Python and Rust against the same exact tree and require byte/semantic parity;
4. preserve deterministic ordering, source digests, trailing-newline behavior, and public artifact formats initially;
5. switch the kind smoke only after independent Rust evidence is green;
6. remove obsolete Python entry points only after the final Rust path is authoritative and exact-head tested.

Changing implementation language does not authorize changing namespace policy, destructive cleanup, provider mutation, or ownership rules.

## Existing work that should not be duplicated

- **DEN-841** already owns evaluation of microVM-backed Kubernetes isolation, including Kata/Firecracker/gVisor comparison and RuntimeClass policy. Local-runtime follow-ups may supply a reusable test substrate, but must not create a second microVM program.
- **DEN-1032** remains the product-neutral three-cluster K3s/recovery parent. The issues above are components of that platform, not replacements for its mesh, GitOps, backup/restore, WAN-partition, secret-rotation, observability, and cloud-migration acceptance criteria.
- **DEN-2786** remains the authority for ownership-aware `dd/` namespace migration. Local kind evidence verifies behavior; it does not declare the migration complete.
- **DEN-1537** remains complete for the reviewed GitHub App bootstrap software contract. `k8s-cluster#886` owns the remaining AWS OIDC trust and hydration proof.

## Recommended execution order

1. **Restore repository-secret hydration:** use `k8s-cluster#886` to repair or provision the trusted-main AWS OIDC role, rerun hydration, verify only the repository secret names, and require `#1540`'s private-backend lane to execute and pass.
2. **Unify local evidence:** implement `#1547` so DEN-1032 and DEN-2786 share one RuntimeProfile/evidence vocabulary with TJSV parity.
3. **Expand platform coverage:** implement `#1548` and `#1549` against the unified contract. They may proceed in parallel after the authority/evidence shape is stable.
4. **Reduce Python:** implement `#1550` with Python↔Rust golden parity before switching CI callers.
5. **Resume the broader DEN-1032 failure/recovery matrix:** use the same contract to add multi-cluster mesh, reboot/site/WAN/secret/storage/rollback/restore tests without creating product-specific forks.

## Evidence and promotion rules

A green local-kind or Multipass run proves only the surfaces it actually exercised. Do not infer:

- EC2 or Hetzner metadata/IAM/storage/network/controller behavior;
- real cloud load-balancer semantics;
- provider billing/capacity behavior;
- production stateful recovery;
- multi-site WAN behavior;
- application-specific consistency guarantees.

Each claim needs an executable test at the appropriate layer. Local verification should stay credential-free whenever provider state is unnecessary; provider certification remains separately gated and should use test-scoped identities.

## Cross-system tracking

Canonical Linear parents:

- DEN-1032 — reusable local K3s platform and recovery harness;
- DEN-2786 — ownership-aware namespace migration;
- DEN-1537 — GitHub App private-backend CI recovery software contract, completed; AWS trust/hydration proof remains external;
- DEN-723 — Daedalus fleet integration carrier that currently contains `#1540`.

GitHub execution surfaces:

- `ORESoftware/k8s-cluster#886` — trusted-main AWS OIDC role/trust and repository-secret hydration recovery;
- `ORESoftware/k8s-cluster#1540` — current exact-head Daedalus/namespace/local-kind carrier;
- `ORESoftware/k8s-cluster#1543` — RuntimeProfile/TJSV local runtime contracts;
- `ORESoftware/k8s-cluster#1547` — unified RuntimeProfile/evidence contract;
- `ORESoftware/k8s-cluster#1548` — arm64/amd64 parity;
- `ORESoftware/k8s-cluster#1549` — kubeadm/containerd Multipass parity;
- `ORESoftware/k8s-cluster#1550` — Rust namespace verifier migration.

This roadmap does not authorize provider writes, production deployment, secret-value access, token rotation/revocation, or destructive Git/history operations.
