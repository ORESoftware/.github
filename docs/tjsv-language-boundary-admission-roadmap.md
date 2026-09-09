# TJSV language-boundary admission rollout roadmap

Status: active program, 2026-09-09  
Primary tracking context: Linear `DEN-3830` and GitHub issue `ORESoftware/.github#36`

## Why this program exists

`ORESoftware/api-docs` now has two independently exercised consumer paths through the public `ORESoftware/typespec-json-schema-validator` (TJSV) language-boundary verifier:

- `api-docs#71` merged as `bda6ed6a318f7b7d5d3390fb3eb738804e996adc` and proves the four-runtime form-profile admission path.
- `api-docs#72` merged as `0afc518e6329f451b5401551ada6452607f0f089` after all eight exact-head pull-request workflows passed. Its tested head was `4372d19c11e5ed4c8a80195f53d030ee49c9e660`, pinned to TJSV `4740f1367a7906813dcd420a77d0c9ede26943fb`.

The #72 retained receipt covered three executed runtime targets across two languages, 140 wire cases, 85 field cases per runtime, eight runtime negative controls and four boundary negative controls, with zero boundary findings. It explicitly records `browserDomOrLiveServer: false`, `arbitraryProductContractsCovered: false`, and `universalEquivalenceProven: false`. The retained artifact was `tjsv-form-4372d19c11e5ed4c8a80195f53d030ee49c9e660`, artifact ID `10116566882`, digest `sha256:eb8577d4d7511176f5035afe33b10619fedc305ca9d64a11625c6d74050f5f03`.

Those results are a foundation, not a claim that every ORESoftware language, platform, transport, build, package, release, or deployed service has been proved.

## Non-negotiable authority model

TypeSpec and human-authored JSON Schema/OpenAPI are independent, human-maintained peer top-level authorities.

Correct model:

- TypeSpec independently owns its authored lane and may produce TypeSpec-side normalized IR, SQL, Protobuf/gRPC and wire-client projections.
- JSON Schema Draft 2020-12/OpenAPI independently owns its authored lane and may produce JSON/HTTP normalized IR, interfaces/types/validators, SQL and write-client projections.
- TJSV compares the independent authorities and verifies retained downstream evidence.
- Generated JSON Schema witnesses, Contract IR, Protobuf/WIT, generated clients, compiled code, runtime observations, transport traces, provenance attestations and receipts are evidence/projections. None becomes a third editable authority.

Any unexplained mismatch remains `STOPPED_FOR_EVALUATION`. No source, generator, runtime, or receipt wins by fallback.

## Evidence strength must remain explicit

A green lower-level receipt must not be silently promoted into a stronger claim. The program should keep distinct evidence layers:

1. **Peer-authority parity** — independent TypeSpec and authored JSON Schema/OpenAPI converge under the declared scope and corpus.
2. **Contract IR admission** — the parity-bound IR is complete for the declared boundary and has no unexplained excluded/out-of-scope declarations.
3. **Runtime/language boundary** — real runtime consumers execute ingress and egress against the same contract/corpus and bind their observations to exact evidence.
4. **Platform-qualified boundary** — runtime evidence is qualified by OS/architecture/ABI/WASM target rather than implicitly generalized from Linux x86_64.
5. **Live transport/browser** — raw HTTP/WebSocket/browser/server boundaries are exercised separately from already-parsed JSON values.
6. **Build/executable provenance** — compiled artifacts are bound to exact source, locks, toolchains, target and output digest, with reproducibility evidence where required.
7. **Release-qualified promotion** — package/release/deployment promotion verifies the exact required evidence profile for the release artifact and commit.

Higher layers may depend on lower layers, but they do not rewrite what an earlier receipt meant.

## Executable backlog

GitHub issue `ORESoftware/.github#36` is the program index. The following child issues are intentionally scoped to residual gaps rather than duplicating broad existing Linear work.

| GitHub issue | Work package | Primary existing Linear context | Outcome |
| --- | --- | --- | --- |
| `#37` | Package TJSV language-boundary verification as the canonical reusable CI admission | DEN-3830, DEN-3959 | Consumer repos use one pinned, fail-closed admission contract instead of bespoke wrappers. |
| `#38` | Add live HTTP/WebSocket/browser boundary evidence above parsed-value receipts | DEN-3830, DEN-3828, DEN-3045 | Real raw transport and browser/server evidence is bound separately from runtime-value evidence. |
| `#40` | Bind boundary receipts to reproducible build and executable provenance | DEN-1713, DEN-2847, DEN-2849, DEN-2851 | Stronger profiles bind exact binaries/build outputs without overloading the existing observation digest. |
| `#43` | Expand the canonical boundary matrix to Go and Gleam native consumers | DEN-3958, DEN-3828, DEN-2253 | Rust, TypeScript, Dart, Go and Gleam have real executable boundary evidence in the strongest fleet profile. |
| `#46` | Certify receipts across OS, architecture and WASM target profiles | DEN-2849, DEN-3045, DEN-3958 | Linux/macOS/Windows/ARM64/WASM coverage is explicit and non-vacuous. |
| `#54` | Define named assurance profiles and claim vocabulary | DEN-3830, DEN-3959, DEN-3043 | `passed` always names the exact evidence profile and cannot be overinterpreted. |
| `#55` | Automate safe validator/toolchain/receipt-schema drift upgrades | DEN-3982, DEN-3043, DEN-3959 | Fleet pins stay immutable but upgrade PRs are discovered and tested automatically. |
| `#57` | Gate package/release/deployment promotion on current boundary receipts | DEN-3495, DEN-1713, DEN-2851, DEN-3959 | Evidence becomes a release blocker rather than an advisory report. |
| `#60` | Aggregate boundary receipts into a non-vacuous fleet evidence ledger | DEN-3982, DEN-3043, DEN-3440 | Fleet status distinguishes passed/stale/missing/zero-step/failed/unsupported/unverified with links to primary evidence. |
| `#63` | Add mutation, fuzz and vacuity resistance to boundary admission | DEN-3830, DEN-3828, DEN-3959 | Empty or non-discriminating corpora/manifests cannot produce misleading green evidence. |

Existing Linear work such as DEN-3958 (SDK-language enforcement), DEN-3959 (dual authorities), DEN-3043 (fleet linting), DEN-3828 (cross-language compiler/conformance runner), DEN-3982 (recurring fleet cross-check) and the existing provenance tickets remains authoritative for its broader scope. These GitHub issues should link to and reuse that work rather than fork it.

## Recommended execution order

### Phase 0 — standardize what a receipt means

1. `#54` assurance-profile registry and claim vocabulary.
2. `#37` canonical reusable admission action/workflow using the reviewed TJSV verifier.
3. Prove the reusable path in at least one real `*-interfaces`/`*-clients` family before bulk rollout.

### Phase 1 — broaden executable coverage

4. `#43` Go + Gleam first-class runtime evidence.
5. `#46` platform-qualified OS/architecture/WASM matrix.
6. `#63` mutation/fuzz/vacuity gates applied to the canonical profile and consumer examples.

### Phase 2 — prove stronger real-world boundaries

7. `#38` raw HTTP/WebSocket/browser/live-test-server evidence.
8. `#40` build/executable provenance integrated with existing Sigstore/SLSA and artifact-provenance work.

### Phase 3 — make the evidence operational fleet-wide

9. `#55` exact-pin drift discovery and upgrade PR automation.
10. `#60` durable fleet evidence ledger and status vocabulary.
11. `#57` package/release/deployment promotion gates consuming the declared assurance profile.

## Fleet rollout rules

- Never replace an immutable TJSV revision with `main`, `latest`, a branch name or an unreviewed tag in promotion evidence.
- Never treat a skipped runtime, unsupported platform, zero-step Actions job, missing artifact or expired receipt as `passed`.
- Never reuse a receipt from another repository, commit, target, corpus, Contract IR or release artifact.
- Keep generated output read-only and regenerable from reviewed sources.
- Preserve exact toolchain/platform identities in evidence, but do not dump secrets or broad environment state.
- A failed upgrade remains blocked; do not silently fall back to an older validator while claiming the newer profile passed.
- Historical receipts remain historical evidence. They do not automatically certify current `main`.
- Release/deployment gates must verify the exact release commit and, for stronger profiles, the exact artifact digest.

## Linear synchronization note

On 2026-09-09 an attempt to create a new Linear program issue was rejected because the workspace had reached its current issue-count limit. No new Linear issue identifier was fabricated. Until capacity is available, `ORESoftware/.github#36` and its child issues are the executable task records; DEN-3830 should carry the cross-link and evidence updates, and this document is the durable portfolio roadmap.

When Linear capacity is restored, create or map work packages only where they add ownership/status value; do not duplicate existing DEN-3958/DEN-3959/DEN-3043/DEN-3828/DEN-3982/provenance scopes merely to mirror GitHub issue count.

## Completion definition

This program is not complete because one sample consumer is green. Completion requires the agreed assurance profiles to be reusable, non-vacuous, platform/runtime qualified, integrated with the selected real product families, represented in the fleet evidence ledger, and enforced at the release boundary where policy requires them. Every stronger claim must remain traceable to exact retained evidence.