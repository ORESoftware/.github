# TJSV discovery wave 6 — namespace identity and real gRPC runtime evidence — 2026-09-09

Tracking: Linear `DEN-3043`, `DEN-3914`, `DEN-3959`, `DEN-3830`, `DEN-3828`; GitHub program `ORESoftware/.github#36` and bounded discovery `#107`.

## Authority invariant

Human-authored TypeSpec and independently human-authored JSON Schema/OpenAPI remain peer top-level authorities. `ORESoftware/typespec-json-schema-validator` (TJSV) is the required convergence/admission implementation for applicable cross-language/runtime boundaries. Generated JSON Schema, Contract IR, Protobuf/gRPC descriptors, SDKs, runtime validators, adapter output and receipts are downstream evidence only.

No lane wins by fallback. Any unexplained structural, behavioral, source-identity, runtime or evidence mismatch is `STOPPED_FOR_EVALUATION` and blocks promotion.

## Discovery that changed implementation

While hardening TJSV PR `#109`, the official TypeSpec compiler history for upstream PR `microsoft/typespec#4050` established an important namespace rule: compact namespace syntax inside an enclosing or blockless/file namespace is lexical. A repeated enclosing prefix creates another nested namespace; it is not an absolute alias.

TJSV's prior `combineNamespace` shortcut violated that rule by dropping a child prefix when it equaled or started with the parent. The corrected TJSV branch now:

- always composes a child declaration/namespace lexically when a parent namespace exists;
- tests repeated dotted nested namespaces;
- tests deeper repeated compact namespaces;
- tests a declaration named exactly like its namespace (`Demo.Demo`);
- tests repeated compact namespaces after a blockless/file namespace;
- asks the official compiler to resolve the expected semantic identities and reject the old shortened identities.

Do not promote the fix until the exact proposed TJSV head is green on the required Ubuntu 24.04 and macOS 14 matrix and satisfies review/comment/thread gates from `ORESoftware/my-ai/AGENTS.md`.

## Capped wave-6 task set

This wave intentionally uses two of the three available discovery slots. The third remains unallocated until another finding survives deduplication.

### Task 1 — `#201`: recertify TJSV consumers after namespace correction

Recertify at least 20 active TJSV consumers across at least 5 GitHub organizations after the validator fix lands.

Required per-consumer evidence:

- exact source revision and TJSV revision;
- independently authored TypeSpec and Draft 2020-12 JSON Schema/OpenAPI source digests;
- current-input parity/differential receipt;
- admissible Contract IR identity;
- required language/runtime evidence;
- exact CI run and finding count;
- explicit failure for stale pre-fix shortened namespace identities.

Prioritize `*-interfaces`, `*-clients`, RPC, middleware, shared-auth and public-core boundaries. Missing evidence is `not-yet-verified`, never green.

### Task 2 — `#202`: execute DEN-3914 gRPC control contracts in real runtimes

Preserve the valid semantic intent from red TJSV PR `#90`, but do not merge red history. Carry unique fixtures/tests forward on current TJSV and execute one trusted corpus through Go, Rust, TypeScript/Node.js and Dart adapters where implementations exist.

Every required runtime receipt must bind to one exact source revision, parity receipt and admissible Contract IR; prove ingress/egress validation; retain normalized verdict/output/stable-error evidence; and reject stale/missing/mismatched evidence.

Protobuf/gRPC remains TypeSpec-lane transport evidence rather than a third authority. Required negative controls include enum drift, requiredness drift, protobuf field/compatibility drift, cross-revision receipt mixing, missing validation execution, normalized-output divergence and stale namespace identity replay.

## Red/stale PR handling

Follow `agents.md`, `docs/stale-and-red-pull-requests.md`, and `ORESoftware/my-ai/AGENTS.md`:

1. Diagnose from exact-head CI/log evidence.
2. Merge current `main` into a salvage branch when needed; do not rebase.
3. Preserve unique tests/contracts/hardening rather than merging a red or stale branch wholesale.
4. Resolve substantive conflicts semantically using the merge base, both heads, tests, contracts and related Linear/GitHub context.
5. Re-run the complete applicable gates at the exact proposed head before merge.

Current classification:

- TJSV `#109`: active fix branch; exact-head CI is required before merge.
- TJSV `#90`: red exact head; not merge-ready; semantic fixture intent is assigned to `#202` for salvage/current-head execution.
- TJSV `#68`: draft and not mergeable; no merge claim.

## Linear synchronization

A dedicated Linear child was attempted for the consumer-recertification follow-on, but the workspace currently rejects new issues because its issue-count limit has been reached. Do not invent DEN identifiers.

Until capacity returns:

- `DEN-3043` is the Linear coordination record for `#201` and contains the recertification acceptance slice;
- `DEN-3914` is the Linear coordination record for `#202` and contains the real-runtime TJSV evidence acceptance slice;
- GitHub `#201` and `#202` are the executable task records;
- existing duplicate-safe Linear backfill/reconciliation should create dedicated children later only if capacity returns and no newer ticket already owns the work.

## Promotion order

1. Land TJSV namespace semantics only after exact-head green/review-clean evidence.
2. Recertify representative consumers and prove stale namespace evidence fails closed.
3. Salvage the DEN-3914 gRPC control fixture onto current TJSV rather than merging red PR `#90`.
4. Execute the same admitted corpus through real runtimes and bind receipts to the exact parity/Contract IR chain.
5. Feed exact scoped receipts into fleet aggregation; do not infer organization/fleet completeness from partial samples.
