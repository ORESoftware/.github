# GitHub organization Projects and certified artifact ledger — 2026-08-05

## Source-of-truth contract

- GitHub repositories, reviewed commits, pull requests, Actions runs, release assets, and retained workflow artifacts are authoritative for implementation and delivery evidence.
- Linear projects are authoritative for planning, ownership, dependencies, milestones, status, and blockers.
- Each registered GitHub organization has one canonical Project titled `<org>-project`, normally project `1`.
- Organization routing documentation lives in the public `<org>/.github` repository and links the organization Project to its canonical Linear project.
- Fleet reconciliation is complete only when every registry organization validates exactly once. Partial, rate-limited, malformed, skipped, or credential-blocked records are failures.
- Credentials are delivered only through protected secrets or nonce-specific RSA-OAEP handoffs. Plaintext credentials are never committed, logged, placed in issue text, or accepted as workflow inputs.

## Certified Zed package publication workflow

The reusable certification and publication workflow was reviewed in `zed-pkg/zed-interfaces#42` and merged at immutable revision:

`d36ac522915792539740cb105e928652503dfde2`

Downstream interface repositories pin that merged revision. Successful runs validate the canonical package, language-specific payloads, deterministic checksums, and provenance before retaining an Actions artifact.

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

ClipTown also fixes Buf release lookup by passing the read-only workflow token to the pinned setup action while preserving its native and generated-language matrices.

## Publication branches blocked before tests

The following exact heads fail before their first executable step. All failed workflows were explicitly re-requested on 2026-08-05; the new attempts again produced `steps: null`, no job logs, and skipped publication jobs. They remain blocked rather than merged without evidence.

| Organization | Pull request | Exact head | Tracking |
|---|---|---|---|
| `messaging-intel` | `msgint-interfaces#24` | `1b64a2149c78208a940b1af51e66bfd77cabd9fc` | GitHub issue `#25`, Linear `DEN-2322` |
| `quaestor-ledger` | `quaestor-interfaces#7` | `1189e19c1d8a7ea35c99e5da0596672be6a49bd7` | GitHub issue `#8`, Linear `DEN-2323` |
| `scintilla-run` | `scintilla-interfaces#13` | `dc8f4c5f5ccb5695b4af54557e4b34300120b1a7` | GitHub issue `#16`, Linear `DEN-2344` |
| `shared-auth` | `shared-auth-interfaces#14` | `91aba0233a96962497a3453ae9fb8b9f973a318a` | GitHub issue `#15`, Linear `DEN-2347` |
| `sonus-auris` | `sonus-auris-interfaces#22` | `087fe6e524c95d022811733e8e69603ed32985c8` | GitHub issue `#23`, Linear `DEN-2351` |

The required response is to restore Actions admission and downloadable diagnostics, then rerun the same exact heads. Required checks must not be converted into skips.

## Organization Project and documentation reconciliation

Trusted-main run `31033274687` is invalid evidence. It emitted only 26 records and accepted GitHub API rate-limit JSON as `canonical_org` while marking records successful.

`ORESoftware/k8s-cluster#992` merged the fail-closed, rate-aware validator at `999693ece857e145e3202f61f3e1eea1f3b0ff43`. A protected-environment run then proved the configured token secret was empty and stopped before mutation.

The canonical mainline now uses a nonce-specific RSA-OAEP-SHA256 handoff and idempotent managed-Markdown reconciliation. An authenticated run, `31037622675`, has completed credential binding and its contract suite and is inside the strict 64-organization reconciliation loop. It remains active while GitHub restores the user token's REST/GraphQL budget.

`ORESoftware/k8s-cluster#1008` merged the quota-aware combined workflow at:

`51aeeca6f4e21cf706104083c384dd876a74026c`

Its trusted-main run `31038213318` is queued behind the active reconciliation because the fleet workflow is intentionally non-concurrent. When it starts, the workflow will wait for both REST Core and GraphQL quota before identity verification and mutation.

Completion requires:

- exactly 64 unique validated registry organizations;
- canonical `<org>-project` title and Project URL;
- public `<org>/.github` repository;
- managed `docs/PROJECTS.md` and `profile/README.md` blocks;
- merged documentation PR or verified unchanged state;
- open governance issue attached to the canonical Project;
- final `VALID evidence=64 expected=64` and a retained `fleet-reconciliation-*` artifact.

Fleet-wide Project/docs completion remains in progress until that proof exists.

## Missing sealed repositories

Four reviewed HypeSiege/StreemPilot identities remain the create-only target set:

- `StreemPilot/streempilot-media-router.rs`
- `hypesiege/hypesiege-scheduler.rs`
- `hypesiege/hypesiege-publishing-worker.rs`
- `hypesiege/hypesiege-analytics.rs`

The AWS-hosted GitHub CLI profile failed before mutation because its profile was unreadable. The empty protected-environment fallback was closed without merge. The combined workflow merged in #1008 now exports the encrypted credential to both `GH_TOKEN` and `GITHUB_REPOSITORY_ADMIN_TOKEN`, runs the unchanged sealed missing-only publisher, and requires:

- only absent private repositories are created;
- all existing repository IDs and `main` SHAs remain unchanged;
- every requested repository is private, has default branch `main`, and has an exact 40-hex head;
- final `VERIFIED_REQUESTED_GAPS 4/4` evidence is retained.

Repository creation has not yet been claimed complete; the combined run is queued behind the active Project/docs pass.

## Follow-through

1. Allow the active rate-aware reconciliation to finish or fail closed with evidence.
2. Deliver one fresh ciphertext to the queued combined run after it publishes its public key.
3. Commit validated Project/docs and repository-creation evidence through a reviewed PR.
4. Append final run IDs, Project URLs, governance issues, repository IDs, head SHAs, artifact IDs, and digests to this ledger and the linked Linear document.
5. Close blockers only after the same exact heads have real successful Actions jobs.
