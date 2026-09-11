# Repository-root TOML runtime configuration contracts

Tracking: `DEN-3959`  
Public task: `ORESoftware/.github#209`

This document defines the public-safe contract for repository-root runtime configuration files used across ORES-managed repositories. Private repository assignments, exact consumer PRs, authenticated inventory, and infrastructure blockers belong in Linear or another approved private system rather than this public repository.

## Authority model

Configuration is split by concern. A domain TOML file is an orchestration/runtime-policy surface for that concern; it is not permission to create another argv parser or collapse cross-runtime contract authority into generated code.

For every normalized configuration contract that crosses language/runtime boundaries:

1. human-authored TypeSpec is one top-level authority;
2. independently human-authored JSON Schema Draft 2020-12/OpenAPI is a peer top-level authority;
3. `ORESoftware/typespec-json-schema-validator` (TJSV), pinned to an immutable reviewed commit, compares/admit the two lanes fail-closed;
4. generated JSON Schema, Contract IR, generated clients/types, normalized JSON, runtime projections, fixtures, and receipts are derived evidence only.

An unexplained mismatch blocks promotion. A zero-step GitHub Actions job is a runner/admission failure, not a pass and not evidence of a source-code defect.

## Canonical filename and owner registry

Repository-root runtime configuration uses a reviewed namespace. A syntactically valid typo such as `.ores-ratelimit.toml` is not a new contract: it is an unregistered filename and must fail closed in portfolio policy checks.

| File | Owning implementation / contract | Responsibility |
| --- | --- | --- |
| `.cli-flags.toml` | `flags-2-env/flags-2-env` | Sole public argv/alias/type/default/CLI-vs-environment precedence contract for executables. |
| `.ores-otel.toml` | `ores-otel` contract family | OpenTelemetry/logging/tracing runtime projection and non-secret telemetry configuration. |
| `.ores-chat.toml` | `ores-chat` contract family | ORES Chat runtime/provider orchestration and non-secret environment-key metadata. |
| `.ores-forms.toml` | `ores-forms` contract family | ORES Forms runtime/validation projection and environment-key metadata. |
| `.opto-sync.toml` | `opto-sync` contract family | Client/server sync projection, stores, background behavior and bounded synchronization policy. |
| `.ores-mw.toml` | `ORESoftware/ores-middleware` | Middleware target/role orchestration, propagation and server-stack selection. |
| `.ores-rl.toml` | `ores-rate-limit` | Rate-limit policy/backend projection and client/server configuration. |
| `.ores-lru.toml` | `ores-redis-lru-cache` | Local/Redis LRU cache projection, namespace and reconciliation configuration. |
| `.shared-auth.toml` | `shared-auth/shared-auth-interfaces` | Canonical Shared Auth repository binding and immutable interface pin. |
| `.auth-shared.toml` | Shared Auth compatibility alias | Compatibility spelling only. It must never coexist with `.shared-auth.toml`; new consumers use the canonical filename. |
| `.fanwaave-cfg.toml` | `fanwaave` | Fanwaave domain/runtime configuration. |
| `.ores-rpc.toml` | `ORESoftware/api-docs` | RPC client/server/hybrid target orchestration, transport/framing selection and environment-key references. |
| `.ores-sidecar.toml` | `ORESoftware/ores-sidecar.rs` | Sidecar identity, immutable listener policy and allowlisted runtime-update keys; Redis transport remains in `.ores-lru.toml`. |
| `.ores-legal.toml` | `ores-legal` contract family | Legal-document/runtime tooling policy and bounded contract metadata. |
| `.ores-wasm.toml` | ORES WASM loader contract family | Shared WASM loader/admission/runtime projection. |
| `.indiebuild.toml` | `gha-indie-worker` / Indiebuild contract family | BYOC/private-SaaS build/deployment orchestration metadata. |

The filename registry is deliberately explicit. A consumer must not invent a second spelling, duplicate a concern under another root file, or silently ignore an unregistered `.ores-*.toml` file. Adding a concern requires an owner, documented authority boundary, tests, and a corresponding portfolio-policy registration.

## `flags-2-env` boundary

`.cli-flags.toml` and the official `flags-2-env` runtime binding own argv parsing. Domain TOML files may reference that contract but must not become competing flag schemas.

Executable startup follows this model:

```text
argv -> flags-2-env audit/parse using .cli-flags.toml
ambient environment -> typed resolution
concern TOML defaults/metadata -> bounded fallback where the owning contract permits it
resolved immutable configuration -> application/core
```

The exact precedence rules must be declared by the executable's approved `flags-2-env` contract and owning concern contract. A domain parser must not silently fall back to its own CLI parser after `flags-2-env` rejects input.

Rules:

- unknown flags and invalid typed values fail startup;
- credentials, tokens, Redis URLs containing secrets, database URLs, private keys, and comparable secret-bearing values are environment/secret-store only and are not CLI flags;
- domain TOMLs may carry environment-variable **names** and bounded metadata, never the secret values themselves;
- a secret binding cannot be argv-exposed and cannot have a plaintext default;
- a concern that allows a non-secret value to be exposed through argv must point to the repository-root `.cli-flags.toml` rather than defining aliases/defaults itself;
- direct ad-hoc `std::env`, `process.env`, `Platform.environment`, or equivalent parsing must not remain a second configuration authority when the executable has adopted `flags-2-env`.

## `ores-cli` portfolio-policy boundary

`ORESoftware/ores-cli` is the portfolio policy consumer and composition linter. It is not a replacement authority for any concern schema.

An admitted `oresc` build should separate the following checks:

- `oresc audit repo --path <repo> ...` — repository structure, root TOML syntax and file safety, the registered runtime-TOML filename set, security-critical cross-file composition invariants, and concern-specific policy checks that are safe to duplicate fail-closed;
- `oresc audit env --path <repo>` — declared environment names versus repository code/config references, required-live-environment policy, encrypted `env/enc` key-shape coverage when the SOPS extension is admitted, and secret-safe reporting;
- `oresc audit contract ...` — delegates TypeSpec/JSON Schema parity and admission evidence to TJSV rather than reimplementing TJSV;
- `.cli-flags.toml` parsing/audit — delegates to the official `flags-2-env` implementation rather than creating a second argv parser.

A portfolio linter may duplicate a security invariant such as “a loopback-only sidecar cannot bind `0.0.0.0`” or “a secret-looking runtime key cannot be dynamically allowlisted,” but the owning implementation and its peer TypeSpec/JSON Schema authorities remain the schema/runtime authority. Ores-cli findings are composition/admission evidence.

Unknown root files matching `.ores-*.toml` fail closed until registered. This prevents a typo or unofficial concern file from being valid TOML yet bypassing every domain linter.

## Environment declarations

Concern contracts may support typed environment references such as:

```toml
flagsContract = ".cli-flags.toml"

[[env]]
name = "apiBaseUrl"
env = "API_BASE_URL"
valueType = "url"
required = true
secret = false
allowArgv = true

[[env]]
name = "serviceCredential"
env = "SERVICE_CREDENTIAL"
valueType = "string"
required = true
secret = true
allowArgv = false
```

This declares names and metadata only. It must not serialize the current environment value into Git, CI artifacts, generated files, logs, PRs, or TJSV evidence.

Owning schemas should reject duplicate logical names, duplicate environment keys where ambiguous, invalid/bounded type metadata, unknown fields, unsafe defaults, and secret-as-argv declarations.

## Client/server repository roles

Every concern that has different client and server capabilities should represent roles explicitly rather than infer them from path names.

Supported repository shapes are:

- `client-only` — client propagation/local policy only; server-only Redis/HMAC/admin implementation must not leak into the projection;
- `server-only` — server runtime policy; client-only endpoint/propagation fields are absent unless the owning contract explicitly supports them;
- `hybrid` / combined — explicit client and server projections in one repository.

A hybrid repository may intentionally place client and server code in the same root. That overlap must be declared explicitly, and path-based target inference must fail as ambiguous rather than guess a role.

Conceptually:

```toml
repositoryMode = "hybrid"
allowOverlappingRoots = true

[[targets]]
name = "server"
role = "server"
roots = ["."]

[[targets]]
name = "client"
role = "client"
roots = ["."]
```

The exact field vocabulary belongs to the concern's peer-authority schemas; this example only illustrates the role invariant.

## Concern boundaries

### Middleware — `.ores-mw.toml`

Middleware config selects where middleware applies and which admitted server stack/propagation projection is used. It does not absorb rate-limit, cache, Shared Auth or RPC wire schemas. Optional env metadata must remain bound to `.cli-flags.toml`/`flags-2-env` and must never carry secret values.

### Rate limit — `.ores-rl.toml`

Rate-limit config owns algorithm/policy/backend projection. Redis remains authoritative where the selected distributed mode requires it. HMAC/Redis references are environment-key names only. Client views must not expose server secret/backend fields. Landing a config in `observe-only` mode does not claim enforcement is active.

### Redis LRU — `.ores-lru.toml`

LRU config owns local/Redis cache behavior, namespaces, Pub/Sub/reconciliation and role projections. Client-only configurations may remain local-only. Server Redis configuration uses environment-key references and must not store credentials. Cache state is not an authority for unrelated rate-limit counters, auth identity or business data.

### Shared Auth — `.shared-auth.toml`

`.shared-auth.toml` is the canonical Shared Auth repository-root binding. `.auth-shared.toml` remains a compatibility alias for already-migrating consumers only. The two filenames must never coexist: consumers fail closed instead of merging two documents or selecting one by precedence.

The binding contains owner/revision and non-secret projection metadata; it must not become a second identity store, token store, or argv authority.

### Sidecar — `.ores-sidecar.toml`

Sidecar config owns sidecar identity, immutable listener settings, runtime namespace and the allowlist of non-secret runtime keys that may change dynamically. `runtimeUpdates` uses `ores-redis-lru-cache` in server role and points to the repository's `.ores-lru.toml`; Redis credentials and transport details stay in the LRU concern.

Security-critical portfolio checks should fail closed on path traversal, a missing/non-regular referenced LRU config, duplicate sidecar names or runtime keys, invalid/zero ports, loopback-only listeners bound to non-loopback addresses, excessive sidecar/key counts, and secret-looking dynamic keys such as tokens, passwords, private keys, database URLs or credentials. The owner implementation remains the complete schema authority.

### OTel — `.ores-otel.toml`

OTel config owns telemetry projection and safe logging/tracing metadata. Secret exporter credentials remain environment/secret-store values referenced only by name. Telemetry config must not become an application configuration catch-all or expose auth/database credentials in generated evidence.

### ORES Chat — `.ores-chat.toml`

Chat config owns ORES Chat runtime/provider orchestration for its concern. Provider credentials remain secret-store/environment values, not TOML literals or CLI defaults. Cross-language contract fields remain under peer TypeSpec/JSON Schema authority where applicable.

### ORES Forms — `.ores-forms.toml`

Forms config owns runtime/validation projection for the Forms family. Shared form contracts remain independently authored in TypeSpec and JSON Schema and are admitted with TJSV. The runtime file is not a substitute for those authorities.

### Opto Sync — `.opto-sync.toml`

Opto Sync config owns declared local/remote stores, sync/background behavior and bounded policy metadata. It does not own unrelated auth, cache or business-data schemas and does not embed service credentials.

### Fanwaave — `.fanwaave-cfg.toml`

Fanwaave config owns domain/runtime settings. Executables use the official `flags-2-env` binding and `.cli-flags.toml`; `.fanwaave-cfg.toml` may supply bounded non-secret defaults/env-key metadata but does not independently parse argv. Client/server/hybrid projections remain explicit.

### RPC — `.ores-rpc.toml`

RPC config owns where `api-docs` RPC contracts are consumed, explicit client/server targets, supported transports/framing, route-map references and environment-key references. It is not a new RPC wire authority. Client/server overlap is explicit and ambiguous target inference fails closed. Secret env bindings are never argv-exposed.

### Legal — `.ores-legal.toml`

Legal config owns bounded legal-tool/document-orchestration policy. Executable configuration still follows `.cli-flags.toml`; generated legal artifacts do not become executable configuration authorities, and contract/document schemas remain independently reviewable.

### WASM loader — `.ores-wasm.toml`

WASM loader config owns shared loader/admission/runtime projection such as loader identities, lifecycle intent, cache/origin metadata and rollback controls. It must not embed deployment credentials or silently convert generated evidence into the authored contract authority.

### Indiebuild — `.indiebuild.toml`

Indiebuild config owns bounded BYOC/private-SaaS build/deployment orchestration metadata. Cloud credentials, signing keys and registry secrets remain outside Git and are referenced by approved secret/environment bindings only.

## Promotion and CI

A consumer config is remotely certified only when the applicable exact-head checks actually execute and pass. Keep these states distinct:

- `stepful_green` — required jobs executed and passed;
- `source_or_contract_failure` — a job executed and a formatter, compiler, test, TJSV, schema, policy or runtime assertion failed;
- `zero_step_admission` — GitHub recorded a job but no runner step executed;
- `external_dependency_blocked` — the runner executed but an approved private/source/dependency checkout or external gate could not be satisfied;
- `partial` — only some required concern/runtime/provider witnesses are available.

`mergeable=true`, a clean TOML parse, or an owner-level TJSV pass alone is not enough to label a consumer green when its required repository checks are red or missing.

## Fleet rollout rule

Use bounded tranches and preserve repository-specific intent. Before changing an existing config:

1. inspect the current file and linked PR/history;
2. verify the filename is in the reviewed root registry and reject unofficial `.ores-*.toml` spellings;
3. preserve stronger existing enforcement rather than replacing it with a generic observe-only/default template;
4. preserve independently authored TypeSpec/JSON Schema authority and the reviewed immutable TJSV pin/channel;
5. preserve `.cli-flags.toml`/`flags-2-env` as the sole argv boundary;
6. run admitted `oresc audit repo` and `oresc audit env` gates when available, without treating those gates as a schema authority;
7. adapt client/server/hybrid roles to the actual repository layout, including intentional same-root code;
8. run repository-local tests and exact-head hosted checks;
9. merge only stepful green work; keep red/stale work as salvage provenance rather than discarding it.

The private DEN-3959 rollout receipt records exact repositories, PRs, heads/merge SHAs and blocker classes. This public file intentionally does not enumerate private repositories or credentials.
