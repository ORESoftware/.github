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

| File | Owning implementation / contract | Responsibility |
| --- | --- | --- |
| `.cli-flags.toml` | `flags-2-env/flags-2-env` | Sole public argv/alias/type/default/CLI-vs-environment precedence contract for executables. |
| `.ores-mw.toml` | `ORESoftware/ores-middleware` | Middleware target/role orchestration, propagation and server-stack selection. |
| `.ores-rl.toml` | `ores-rate-limit` | Rate-limit policy/backend projection and client/server configuration. |
| `.ores-lru.toml` | `ores-redis-lru-cache` | Local/Redis LRU cache projection, namespace and reconciliation configuration. |
| `.auth-shared.toml` | `shared-auth` compatibility surface | Shared Auth repository-local binding while the owner-controlled canonical-name transition remains under review. Never coexist with another Shared Auth root filename. |
| `.fanwaave-cfg.toml` | `fanwaave` | Fanwaave domain/runtime configuration. |
| `.ores-rpc.toml` | `ORESoftware/api-docs` | RPC client/server/hybrid target orchestration, transport/framing selection and environment-key references. |

The filename registry is deliberately narrow. A consumer should not invent a second spelling or duplicate a concern under another root file.

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

### Shared Auth — `.auth-shared.toml`

`.auth-shared.toml` is the supported compatibility filename requested for current consumers. Shared Auth owner work may define a canonical-name transition separately. Until that transition is fully admitted and migrated, consumers must fail closed on dual root auth filenames rather than trying to merge two configurations or select one by precedence.

### Fanwaave — `.fanwaave-cfg.toml`

Fanwaave config owns domain/runtime settings. Executables use the official `flags-2-env` binding and `.cli-flags.toml`; `.fanwaave-cfg.toml` may supply bounded non-secret defaults/env-key metadata but does not independently parse argv. Client/server/hybrid projections remain explicit.

### RPC — `.ores-rpc.toml`

RPC config owns where `api-docs` RPC contracts are consumed, explicit client/server targets, supported transports/framing, route-map references and environment-key references. It is not a new RPC wire authority. Client/server overlap is explicit and ambiguous target inference fails closed. Secret env bindings are never argv-exposed.

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
2. preserve stronger existing enforcement rather than replacing it with a generic observe-only/default template;
3. preserve independently authored TypeSpec/JSON Schema authority and the reviewed immutable TJSV pin/channel;
4. preserve `.cli-flags.toml`/`flags-2-env` as the sole argv boundary;
5. adapt client/server/hybrid roles to the actual repository layout, including intentional same-root code;
6. run repository-local tests and exact-head hosted checks;
7. merge only stepful green work; keep red/stale work as salvage provenance rather than discarding it.

The private DEN-3959 rollout receipt records exact repositories, PRs, heads/merge SHAs and blocker classes. This public file intentionally does not enumerate private repositories or credentials.
