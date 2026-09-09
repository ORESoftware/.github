# TJSV evidence admissibility wave 5 — revocation and downgrade resistance

Status: active execution map, 2026-09-09  
Primary Linear context: `DEN-3830`, `DEN-3959`, `DEN-3982`, `DEN-3043`  
Parent GitHub program: `ORESoftware/.github#36`  
New executable tasks: `ORESoftware/.github#167` and `ORESoftware/.github#169`

## Why this wave exists

The current TJSV program already covers peer-authority parity, Contract IR,
runtime/language execution, platform qualification, evidence retention, pin
consistency, safe upgrades, release admission, fleet aggregation, dependency
cohorts, exact-head verification, and merge-base drift. Two evidence-admission
states were still not represented explicitly:

1. evidence that was valid when produced but is later affected by a discovered
   validator, toolchain, dependency, runtime-adapter, or verifier defect; and
2. evidence that is internally valid but weaker than the assurance strength the
   consumer or promotion point requires.

Both can otherwise produce a misleading green result. Freshness is not the same
as continuing admissibility, and validator compatibility is not the same as
assurance-profile sufficiency.

## Current canary and deliberate non-action

`ORESoftware/api-docs` currently contains more than one reviewed immutable TJSV
revision across distinct contract and language-boundary paths. The RPC,
request-surface, and projection surfaces still contain the previously audited
revision `d60d0d79d83e075077382623ec9e23a401ab601f`; the newer form-contract and
form-profile language-boundary paths use
`4740f1367a7906813dcd420a77d0c9ede26943fb`.

This wave does **not** bulk-replace those pins or assume that exact equality is
the correct policy. Existing work owns that decision:

- `#75` defines the reviewed release-channel and validator/profile compatibility
  policy;
- `#77` defines the repository-local consumer lock and complete pin/reference
  drift gate;
- `#55` owns exact-head upgrade preparation and recertification.

Until those policies classify the split, the correct status is explicit and
bounded—not an inferred violation and not an unreviewed normalization.

## Duplicate review and existing ownership

The following existing issues remain canonical for their scopes:

| Issue | Existing ownership | Why it was not duplicated |
| --- | --- | --- |
| `#40` | Build/executable provenance | Proves what binary or artifact ran; it does not invalidate a previously valid receipt after a later defect disclosure. |
| `#54` | Named assurance profiles and claim vocabulary | Defines profile contents; it does not compare a consumer minimum against presented evidence or prevent stripping/downgrade. |
| `#55` | Safe TJSV/toolchain/receipt upgrades | Produces remediation candidates; it needs a separate signal explaining that current evidence is quarantined or insufficient. |
| `#57` | Package/release/deployment promotion gates | Consumes evidence decisions; it should not independently invent advisory or profile-dominance semantics. |
| `#60` | Fleet evidence ledger | Aggregates classified evidence; it does not originate revocation or downgrade rules. |
| `#75` | Release-channel and pin compatibility | Decides executable/profile-version compatibility, not whether presented evidence meets the consumer's minimum strength. |
| `#77` | Consumer lock and pin/reference drift | Makes local identity consistent, but consistency can still preserve a known-bad or too-weak evidence choice. |
| `#90` | Independent JSON Schema validator diversity | Adds corroborating lineages; it is one possible required capability, not the general downgrade protocol. |
| `#91` | TJSV production dependency advisories | Remediates dependency vulnerabilities; it does not define post-hoc receipt impact and propagation. |
| `#99` | Retention, expiry, supersession, historical pass | Handles ordinary evidence age/lifetime; a fresh receipt can still require immediate quarantine. |
| `#129` | Base-SHA and semantic-conflict merge readiness | Invalidates merge readiness after base movement; it is orthogonal to TJSV evidence revocation and profile strength. |
| `#135` | Compatibility-derived semver/version-policy decisions | Decides release/version actions after evidence exists; it must consume rather than redefine minimum evidence strength. |
| `#136` | Exact multi-repository dependency cohorts | Prevents mixed-generation composition; every component receipt can still be revoked or too weak. |

No dedicated matching issue was found for post-hoc TJSV receipt invalidation or
for requirement-versus-presented assurance downgrade resistance. The two new
issues below own only those residual gaps.

## Task A — advisory-driven quarantine and revocation

Executable issue: `ORESoftware/.github#167`

### Problem

An exact-head receipt may be unexpired, correctly pinned, internally
self-consistent, and attached to the right source commit when a later defect is
disclosed. Continuing to accept it until natural expiry or a routine upgrade is
unsafe. Deleting or rewriting the receipt would also destroy provenance.

### Required record

Define a versioned advisory record, provisionally
`ores.tjsv-evidence-advisory/v1`, with a closed and digest-bound envelope that
identifies:

- advisory ID, status, severity, owner, discovery time, publication revision,
  and remediation issue;
- exact affected validator commits, toolchain/runtime identities, profile and
  receipt-schema revisions, Contract IR schemas, semantic features, and
  corpus/case fingerprints;
- impact classification: `under_investigation`, `quarantined`, `revoked`,
  `resolved`, or `not_affected`;
- an exact replacement revision and required recertification profile when one
  exists;
- issuer/provenance identity and an immutable canonical digest.

Do not use ambiguous branch names, floating tags, open-ended human prose, or an
unbounded environment dump as impact selectors.

### Admission behavior

- A receipt that matches an active advisory cannot satisfy merge, package,
  release, promotion, or deployment admission even if all ordinary freshness
  checks pass.
- Historical receipts remain immutable and queryable. Their admissibility state
  changes by reference; their original bytes and original result do not.
- Resolving an advisory does not resurrect old evidence automatically. The
  consumer must present fresh exact-head evidence for the reviewed replacement
  revision and required profile.
- Offline verification may use a signed or content-addressed advisory snapshot
  with a profile-defined maximum age. Missing, stale, conflicting, or
  unverifiable advisory state fails closed where advisory checking is required.
- Stable impact fingerprints feed `#60`; exact-pin remediation and
  recertification feed `#55`; promotion vetoes feed `#57`.

### Negative controls

The implementation must reject or classify correctly:

- forged issuer identity or tampered digest;
- stale advisory snapshots and replay of an advisory after resolution;
- ambiguous commit ranges or symbolic refs;
- a wrong repository/profile/schema/corpus scope;
- partial feature impact presented as whole-validator impact, and the reverse;
- conflicting advisories without a deterministic fail-closed resolution;
- an active advisory with no replacement evidence;
- unavailable advisory infrastructure when the assurance profile requires a
  current snapshot.

## Task B — requirement-versus-presented evidence admission

Executable issue: `ORESoftware/.github#169`

### Problem

A syntactically valid receipt can report `passed` while omitting evidence that a
specific consumer requires. Examples include a lower or incomparable profile,
an older unsupported profile revision, fewer runtimes/platforms, disabled
negative controls, an empty validator-diversity lane, stripped receipt fields,
or a fallback to weaker historical evidence.

### Required records

Define two separately digest-bound views:

1. a consumer or promotion-point requirement manifest, provisionally
   `ores.tjsv-evidence-requirement/v1`; and
2. the producer's presented profile/capability inventory, derived from the exact
   executed receipt closure.

The requirement manifest names the minimum profile revision and every required
capability: peer-authority checks, Contract IR completeness, runtime/language
matrix, platforms, transport, validator lineages, format/reference policy,
negative controls, determinism/resource policy, provenance, freshness, and
advisory status where applicable.

### Dominance, not naming heuristics

Satisfaction must use an explicit reviewed dominance graph from `#54`.

- Do not infer strength from a profile name, lexical order, semantic-version
  magnitude, or the presence of unknown fields.
- Profiles may be incomparable. Incomparability is not success.
- A validator revision allowed by `#75` does not imply that its receipt profile
  satisfies the consumer minimum.
- Removing fields from a signed or digest-bound receipt invalidates that receipt
  rather than creating a valid lower profile.
- A fallback path may retain and report weaker evidence, but it cannot mark the
  stronger requirement passed.

Required failure states include `downgrade_rejected`, `incomparable_profile`,
`missing_capability`, `unknown_capability`, `stale_requirement`, and
`stopped_for_evaluation`, each with stable public-safe fingerprints.

### Negative controls

The implementation must cover:

- profile-name spoofing and a higher version number with fewer capabilities;
- omitted, duplicate, contradictory, or unknown capabilities;
- zero-case, zero-runtime, or zero-platform evidence;
- a disabled format/reference/negative-control policy;
- receipt field stripping or unsigned replacement of the requirement manifest;
- replay of a lower-profile historical receipt at a stronger gate;
- an upgrade automation change that weakens the requirement to make CI green;
- a validator compatibility window incorrectly treated as profile dominance;
- advisory-affected evidence that otherwise dominates the required capability
  set.

## Combined state model

Freshness, compatibility, capability strength, and advisory state are independent
axes. A release decision must not collapse them into one Boolean.

| Axis | Representative states |
| --- | --- |
| Source/evidence identity | exact, mismatched, missing, unverifiable |
| Freshness/lifetime | current, stale, expired, superseded, historical pass |
| Validator/profile compatibility | compatible, incompatible, unsupported, unknown |
| Assurance strength | satisfied, downgrade rejected, incomparable, missing capability |
| Defect/advisory impact | unaffected, under investigation, quarantined, revoked, resolved-pending-recertification |
| Execution | passed, failed, stopped for evaluation, nondeterministic, resource-budget-exceeded |

Only an explicitly declared policy may map the complete state vector to a
promotion decision. No individual axis may silently override another.

## Immediate implementation order

1. Complete the canonical profile/capability vocabulary and dominance graph in
   `#54`.
2. Implement `#169` requirement-versus-presented comparison with a small closed
   schema and adversarial fixtures.
3. Implement `#167` advisory matching and impact propagation using the same
   exact identity vocabulary; this can proceed in parallel once identity terms
   are stable.
4. Extend `#75` and `#77` to reference—not copy—the new decisions.
5. Extend `#55` to create exact-pin remediation PRs without weakening required
   profiles or falling back silently.
6. Extend `#60` to expose all independent axes and stable fingerprints.
7. Require the combined decision in `#57` and compatibility/version-policy work
   in `#135`; use `#136` for multi-repository composition.
8. Exercise an end-to-end canary using `ORESoftware/api-docs`, the canonical
   TJSV repository, and at least one separate consumer such as `ores-cli` or
   `ores-gh-bots`.

## Canary acceptance sequence

The first complete canary should demonstrate all of the following without
changing either authored contract authority:

1. produce an exact green TJSV receipt for a reviewed consumer commit;
2. show that the receipt satisfies an exact requirement manifest;
3. publish a test advisory scoped to the exact validator/profile/case closure;
4. show the same unexpired receipt move to `quarantined` without changing its
   bytes;
5. publish an exact replacement validator revision and prepare a focused upgrade
   through `#55`;
6. run the full required profile on the exact remediation head;
7. show that a weaker replacement receipt remains downgrade-rejected;
8. show that the exact qualifying replacement is current, unaffected, and
   admissible;
9. propagate one stable finding/resolution chain through the fleet ledger and
   release gate without duplicate task creation.

## Authority and security invariants

- TypeSpec and independently authored JSON Schema/OpenAPI remain human-maintained
  peer top-level authorities.
- Generated JSON Schema witnesses, Contract IR, Protobuf/WIT, runtime/toolchain
  evidence, profile manifests, advisory records, and receipts remain downstream
  evidence or control records only.
- No source, validator, runtime majority, profile, previous receipt, or fallback
  wins automatically.
- Missing, stale, unknown, downgraded, quarantined, revoked, unsupported,
  nondeterministic, or unverifiable required evidence fails closed.
- Records must never contain credentials, private keys, decrypted secrets,
  private source payloads, customer data, broad environment dumps, or pasted
  access tokens.

## Linear synchronization

A dedicated Linear issue for task A was attempted on 2026-09-09 and rejected
because the workspace remains at its free issue limit. No DEN identifier was
fabricated. The Linear document **TJSV evidence invalidation and
downgrade-resistance follow-through — 2026-09-09** is attached to `DEN-3830`;
`DEN-3830` and `DEN-3959` carry coordination updates while GitHub issues `#167`
and `#169` are the executable task records until issue capacity is available.

## Completion definition

This wave is complete only when a real consumer proves both dimensions:

- a still-fresh receipt can be quarantined or revoked by exact scoped advisory
  evidence and can return to current status only through reviewed replacement
  evidence; and
- a syntactically valid but weaker or incomparable receipt cannot satisfy a
  stronger consumer requirement.

The final evidence must be exact-head, machine-readable, non-vacuous,
content-addressed, public-safe, and consumable by the existing fleet and release
systems without creating a parallel authority or duplicate verifier.
