# TJSV runtime validation convergence — execution wave 3

Status: active, 2026-09-09  
Parent program: [`ORESoftware/.github#36`](https://github.com/ORESoftware/.github/issues/36)  
Primary Linear context: `DEN-3828`, `DEN-3959`, `DEN-3982`, `DEN-3043`

This companion wave starts from a narrower question than the general language-boundary roadmap: after independently authored TypeSpec and JSON Schema/OpenAPI agree, **how do we prove that Zod, Serde-backed Rust, Dart, direct JSON Schema evaluators, and application construction paths enforce the same admitted contract without silently transforming, weakening, or bypassing it?**

It complements [wave 2](./tjsv-execution-wave-2-2026-09-09.md). It does not duplicate reusable CI (#37), independent validator diversity (#90), live browser/transport evidence (#38), fleet receipt aggregation (#60), or the broader Linear programs.

## Verified baseline

The planning baseline is executable evidence, not only intended architecture:

- `ores-otel-test/contract-conformance-tests#7` merged as `9ac9978c3e84136618aea2745d8ddb47c62eb8db` after exact-head runtime-conformance and Deep-suite workflows passed. The canary executed Zod 4.5.4, Serde 1.0.228 + `serde_json` 1.0.145, Dart VM 3.13.3 and dart2js over 41 trusted cases.
- `ORESoftware/ores-interfaces#4` merged as `f9da7718aefd5a95a331c79faa9f0c66a30cdb73`, advancing the shared-interface consumer to the reviewed current source/TJSV closure with Linux and macOS admission green.
- `ores-otel-test/contract-conformance-tests#8` merged as `659f83f9a7fd86743a0bc4b489384f0f99bfa723`. It changed only immutable source/tool pins and recertified the same runtime matrix on `ores-otel/ores-interfaces@09b06c7d82852b657e812a70eeb63023d0aed2a6` and `ORESoftware/typespec-json-schema-validator@d60d0d79d83e075077382623ec9e23a401ab601f`.
- In #8 all four adapters retained exactly the same 41 case/declaration/verdict tuples as the preceding reviewed run. TJSV returned `passed` with zero unexplained findings and 4/4 required/observed/passed adapters. The runtime corpus digest remained `fcb276361dc377f8b780668888dc1c5cfcc2ec5ea6ead1740763f5c3783bd7d2` while IR/run/evidence digests changed with the new verified closure, as expected.

That is strong verdict-parity evidence for one canary. It is not proof that every fleet validator or constructor is bound correctly, that accepted values are normalized identically, that PATCH state is preserved, or that every JSON Schema `format` is actually asserted.

## New specialized work packages

| GitHub issue | Role in the existing program | Required outcome |
| --- | --- | --- |
| [`#65`](https://github.com/ORESoftware/.github/issues/65) | TJSV runtime-evidence protocol extension under DEN-3828 | Runtime evidence can compare canonical admitted outputs and safe stable validation errors, so identical verdicts cannot hide transform/error divergence. |
| [`#68`](https://github.com/ORESoftware/.github/issues/68) | PATCH semantic canary under DEN-3959 | Missing, explicit null and present value remain distinct through parse, validation, update application and read-back in Zod, Serde-backed Rust and Dart. |
| [`#70`](https://github.com/ORESoftware/.github/issues/70) | Explicit format-policy slice of assurance profiles #54 and validator diversity #90 | Required JSON Schema formats have a versioned assertion policy; disabled or unsupported required checks stop evaluation. |
| [`#71`](https://github.com/ORESoftware/.github/issues/71) | Construction/deserialization safety under DEN-3959 | Public constructors and deserializers cannot bypass validation; compile-fail/static protection and runtime rejection are tested separately. |
| [`#76`](https://github.com/ORESoftware/.github/issues/76) | Runtime/test-org specialization of canonical reusable admission #37 | At least three `*-test` orgs consume one immutable reusable TJSV runtime-conformance workflow instead of copying admission orchestration. |
| [`#79`](https://github.com/ORESoftware/.github/issues/79) | Discovery/scanner input to fleet evidence ledger #60 | `ores-cli` inventories real validators, construction boundaries, TJSV gates and paired-test evidence across 100+ repos/20+ orgs without inferring pass from dependencies. |
| [`#82`](https://github.com/ORESoftware/.github/issues/82) | Library-vs-direct-schema canary under validator diversity #90 | Zod/Serde/Dart contract adapters are cross-checked against pinned direct Draft 2020-12 evaluators; unsupported required semantics remain explicit. |

## Dependency and execution order

### Phase A — make runtime evidence semantically complete

1. **#65 first.** Verdict-only receipts are too weak for transformations and stable error behavior. Add canonical output/error evidence while keeping rejected private payloads and library-specific messages out of receipts.
2. **#68 next.** Use the stronger output evidence to prove missing/null/value PATCH state and update/read-back behavior, not merely parse success.
3. **#71 next.** Prove public construction and deserialization cannot bypass the same contract. Feed its discoverable boundary patterns into #79.

### Phase B — cross-check the validators themselves

4. **#70** defines explicit `format` assertion policy as part of the named assurance profile in #54. Do not rely on library defaults.
5. **#90** remains the owner of independent validator diversity. **#82** is its practical product-facing canary: compare library validators with the actual authored Draft 2020-12 schema through independent evaluator lineages.
6. Coordinate Dart/browser execution with existing real-browser work (`DEN-554`) and live boundary #38 rather than inventing another browser harness.

### Phase C — scale the proven gate without copy/paste drift

7. Land canonical reusable admission #37, then **#76** as its runtime-conformance/test-org specialization. Pilot at least three independent `*-test` orgs including a deliberately stale consumer.
8. Implement **#79** in `ores-cli` to discover where the fleet has validators but lacks executed TJSV/constructor/test-org evidence. Keep discovery classification separate from #60's verified receipt ledger.
9. Feed exact current receipts into #60 and recurring fleet CI in DEN-3982. Missing, partial or stale inventory is never promoted to verified evidence.

## Existing work reused rather than duplicated

- `#37` — canonical reusable language-boundary CI admission; #76 is its runtime specialization.
- `#38` — live HTTP/WebSocket/browser boundary evidence; coordinate real Dart/browser execution here.
- `#54` — named assurance profiles and claim vocabulary; #70 contributes the format-policy dimension.
- `#60` — verified fleet receipt ledger; #79 feeds discovery and current receipt references into it but does not replace it.
- `#63` — mutation/fuzz/vacuity resistance; new runtime tasks should contribute adversarial fixtures rather than build a parallel fuzz program.
- `#88` — parsed HTTP response/error/metadata contracts; #65 owns validator evidence/error comparison rather than HTTP response modeling.
- `#90` — independent JSON Schema validator lineages; #82 is the library-vs-direct-evaluator implementation canary.
- Linear `DEN-554` and `DEN-1303` — real browser/cross-browser execution.
- Linear `DEN-1464`, `DEN-1482`, `DEN-1437`, `DEN-3488`, and `DEN-3908` — Zed frozen/install/registry closure; no duplicate packaging ticket is created here.
- `ORESoftware/typespec-json-schema-validator#11` — release/publication and known build-toolchain advisory context; this wave does not create a duplicate advisory task.

## Fleet acceptance rules added by this wave

A runtime validation profile may only be called passed when the declared scope has evidence for all applicable items below:

- current peer-authority parity and verified Contract IR;
- exact runtime/toolchain identities and trusted corpus digest;
- required adapter presence and non-vacuous case execution;
- verdict agreement;
- canonical accepted-output agreement where transformations/output semantics are in scope;
- stable validation error agreement where error semantics are in scope;
- explicit missing/null/value behavior for update contracts;
- public construction/deserialization admission, not only a helper `validate()` call;
- explicit `format` assertion configuration for every required format;
- direct schema evaluator corroboration where the assurance profile requires it;
- platform/browser qualification when claimed;
- exact-current evidence status in the fleet ledger.

A finite corpus remains regression evidence, not a universal proof. An unsupported required comparison remains `STOPPED_FOR_EVALUATION`; no runtime, validator, generated witness, or majority vote can overrule either authored authority.

## Linear synchronization

New Linear issue creation was attempted and rejected because the workspace has reached its issue-count limit. No DEN identifiers were fabricated. The durable Linear mirror for this wave is the document **Validation runtime convergence — next task map (2026-09-09)** attached to DEN-3959. Existing DEN-3828, DEN-3959, DEN-3982 and DEN-3043 remain the ownership/status anchors while these GitHub issues are executable task records.

## Completion definition

This wave is complete when the runtime evidence protocol can catch same-verdict/different-output behavior, PATCH and construction-bypass canaries are green and adversarially discriminating, required formats/direct evaluators are explicit, three `*-test` orgs consume one reusable runtime admission, and `ores-cli` can identify fleet gaps that feed verified exact-current evidence into #60. It is not complete merely because the original 41-case canary remains green.