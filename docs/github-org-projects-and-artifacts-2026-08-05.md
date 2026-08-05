# GitHub organization Projects and certified artifact ledger — 2026-08-05

## Source-of-truth contract

- GitHub repositories, reviewed commits, pull requests, Actions runs, release assets, and retained workflow artifacts are authoritative for implementation and delivery evidence.
- Linear projects are authoritative for planning, ownership, dependencies, milestones, blockers, and current delivery state.
- Each registered GitHub organization has one canonical Project titled `<org>-project`, normally project `1`.
- Organization routing documentation lives in the public `<org>/.github` repository and links the organization Project to its canonical Linear project.
- No fleet reconciliation is complete until its evidence validates every registry organization exactly once. Partial, rate-limited, malformed, skipped, or credential-blocked records are failures rather than successes.
- Credentials pasted into chat, comments, issue bodies, workflow inputs, or source are incident material, not an approved execution channel. They must be revoked and replaced through protected secret or encrypted one-time handoff paths.

## Certified Zed package publication workflow

The reusable certification and publication workflow was reviewed in `zed-pkg/zed-interfaces#42` and merged at immutable revision:

`d36ac522915792539740cb105e928652503dfde2`

Downstream interface repositories pin that merged revision. Each successful run validates the canonical package, language-specific payloads, deterministic checksums, and provenance before retaining an Actions artifact.

## Merged package-publication canaries

| Organization | Repository / PR | Merge SHA | Artifact ID | Artifact SHA-256 |
|---|---|---|---:|---|
| `akrion-sim` | `akrion-sim-interfaces#8` | `9c0282e33f525f8c904bedf1d240680c3a917ba2` | `8941448501` | `b39ba43c49111cefb71bc801e4eed211f7c96ecae48292fdff22eeb4a26f3f03` |
| `anticaptrad` | `act-interfaces#9` | `f7c15676ee9add5429404e893cb0767067a0a450` | `8941409714` | `9564d294da31f020e3609bb36436c93987362d1f90fefb60113be8a63f96c9b7` |
| `athlet-o` | `athleto-interfaces#8` | `13c2c078f758955fcbcd86c7b7a10e1b7e41b9eb` | `8941509994` | `017d04d23a77ad2db64f84129ae26f113d2c6eb98f9f5521d656a2a5fc06d9e9` |
| `benefactor-cc` | `benefactor-interfaces#16` | `c3bbe4f96107effa9b666f6175696c085be7a74e` | `8941454094` | `1f11cad0d824e3ec7f8599ed5e0c218477980450b57668c8d55d375e2e563dba` |
| `canonical-cloud` | `canonical-interfaces#23` | `6c0204c64b752d0f2663a3c2e2f7eb2871c6b4d8` | `8941416193` | `d6d24b7484f104e4590e704188cfddd9ee5eb72a68e4b9a26a746e07d068d20e` |
| `cliptown` | `cliptown-interfaces#12` | `85581536948217b0d9433a900a290eee000bc51c` | `8941428452` | `62e4acd89ca23e98ea853eba4e06f0acb60114313ab216e44647441400ea2ce9` |
| `daedalus-fab` | `daedalus-interfaces#8` | `ed6107713ce1bef4262af6b110e2449ea74e4e22` | `8941480831` | `8b97f6b1f0db01651dc939d721229183394bd41c808536f4a69cef618834b4b5` |
| `fiducia-cloud` | `fiducia-interfaces#50` | `16ba4766b7b8e60f88bb425d5570d77fe0c5c6c3` | `8941440734` | `0b84ea01946e8a3d090d34a6a38f6fb758f231d0895ac31091b82c6b587eac99` |
| `file-tunnel` | `ftnl-interfaces#8` | `22cd738ac574e41b6a04188181387722fe709716` | `8941440263` | `a83e0d3cac967dacd1fde6fd042dc151d30307a9965bfb1d1b1318a556e71b28` |
| `hypesiege` | `hypesiege-interfaces#12` | `e52d76aedabbe7dc4984169486e8305f993796fb` | `8941480253` | `a4f1f43d652a3d1d5505132293315d0ada9ed2fda9f430d0ea56308b2433413a` |
| `voxletra` | `vxl-interfaces#7` | `061645ed7a2dcd43267a85ef546bea64807892c6` | `8941570863` | `045528754357a393de1459321369e2ea2d612402afbb58dcf666ac9a9343ef60` |

The ClipTown publication also fixes Buf release lookup by passing the read-only workflow token to the pinned setup action. The native and generated-language test matrices remain intact.

## Publication branches blocked before tests

The following exact-head publication PRs remain open because GitHub Actions concluded before their first executable step. They must not be merged until real validation and publication jobs execute:

| Organization | Pull request | Exact head | Blocker |
|---|---|---|---|
| `messaging-intel` | `msgint-interfaces#24` | `1b64a2149c78208a940b1af51e66bfd77cabd9fc` | zero-step Actions admission failure |
| `quaestor-ledger` | `quaestor-interfaces#7` | `1189e19c1d8a7ea35c99e5da0596672be6a49bd7` | zero-step Actions admission failure |
| `scintilla-run` | `scintilla-interfaces#13` | `dc8f4c5f5ccb5695b4af54557e4b34300120b1a7` | zero-step Actions admission failure |
| `shared-auth` | `shared-auth-interfaces#14` | `91aba0233a96962497a3453ae9fb8b9f973a318a` | zero-step Actions admission failure |
| `sonus-auris` | `sonus-auris-interfaces#22` | `087fe6e524c95d022811733e8e69603ed32985c8` | zero-step Actions admission failure |

The required response is to restore Actions admission and diagnostic logs, then rerun the same exact head. Required checks must not be converted into skips.

## Organization Project and documentation reconciliation

Trusted-main run `31033274687` is explicitly invalid evidence. It emitted only 26 records and accepted GitHub API rate-limit JSON as `canonical_org` while marking each record successful.

`ORESoftware/k8s-cluster#992` replaced that behavior with a fail-closed, rate-aware reconciler and merged as:

`999693ece857e145e3202f61f3e1eea1f3b0ff43`

Its protected run `31035799241` **failed before mutation** in the credential-binding step because `PROJECT_SYNC_GITHUB_TOKEN` was empty. Contract and checkout steps ran, but organization reconciliation, validation, and artifact publication were skipped. This run is not acceptance evidence.

Current `main` at `9b640895104f7d426dca278f2a06039de56350a0` retires the non-verifiable shell-only path, keeps the strict rate-aware 64-organization validator as the sole canonical reconciliation path, and adds idempotent managed-Markdown helpers so reruns update only controlled blocks.

The live workflow now requires a one-time RSA-OAEP-SHA256 encrypted credential handoff. It validates:

- exact 64-row registry coverage with no duplicates;
- canonical organization identity;
- canonical `<org>-project` title and Project URL;
- public `<org>/.github` repository;
- managed `docs/PROJECTS.md` and `profile/README.md` blocks;
- merged organization documentation PR or a verified unchanged state;
- open governance issue attached to the canonical Project;
- live GitHub API state after each mutation.

Fleet-wide Project/docs completion remains open until a trusted-main run prints `VALID evidence=64 expected=64` and retains the exact evidence artifact.

## Missing sealed repositories

Four reviewed HypeSiege/StreemPilot repository identities remain the explicit create-only target set:

- `StreemPilot/streempilot-media-router.rs`
- `hypesiege/hypesiege-scheduler.rs`
- `hypesiege/hypesiege-publishing-worker.rs`
- `hypesiege/hypesiege-analytics.rs`

`ORESoftware/k8s-cluster#994` was closed without merge after the protected environment token proved empty. It is superseded by `ORESoftware/k8s-cluster#1001`, which reuses the repository's encrypted one-time handoff design and combines strict repository publication evidence with the Project/docs reconciliation.

At the time of this ledger update, #1001 is **not merge-ready**: its dedicated encrypted-fleet contract and secret scan pass, but the shared `repo checks` workflow is red and the branch conflicts with newer idempotent reconciliation changes on `main`. It must be semantically rebuilt on current `main`; neither conflict markers nor pasted credentials may be used as a shortcut.

## Execution state and follow-through

1. Rebuild the create-only sealed-repository workflow on current `main` without replacing the canonical rate-aware Project/docs path.
2. Require exact-head contract, secret-scan, repository-policy, and shared repository checks before merge.
3. Execute repository creation and Project/docs reconciliation only through protected or encrypted one-time credential delivery; never through chat-pasted credentials.
4. Commit validated evidence through reviewed pull requests and retain run/artifact identifiers and SHA-256 digests.
5. Update linked Linear projects with exact run, PR, merge, Project, issue, artifact, and digest evidence.
6. Close blocker issues only after the same exact heads have real successful Actions jobs.
7. Keep organization Projects and Linear routing documents synchronized through managed blocks without overwriting unrelated project history.
