# Deprecated ORESoftware repositories

`deprecated-repositories.json` is the machine-readable authority for repositories
that have moved out of the `ORESoftware` owner. A deprecated repository remains
available only to preserve links, migration history, and bounded transition
support. It must not publish, deploy, receive new product features, or become a
new dependency source.

| Historical repository | Canonical repository | Release authority |
|---|---|---|
| `ORESoftware/ai-agent-bridge.rs` | `agent-pontifex/ai-agent-bridge.rs` | Canonical repository only |
| `ORESoftware/shared-auth-server.rs` | `shared-auth/shared-auth-server.rs` | Canonical repository only |

Every listed historical repository must prepend its README and repository-local
agent instructions with the canonical destination, keep package publication and
deployment disabled, and carry a fail-closed test that rejects deprecation
notice drift. Changes in a historical repository are limited to the exact
machine-readable classes: deprecation maintenance, security remediation,
migration, narrowly scoped compatibility, and historical reference.

New entries require evidence that the destination is operational and contains
the authoritative implementation or an explicit migration plan. The
`ORESoftware/ai-agent-bridge.rs` decision and remaining migration gates are
recorded in
[`docs/migrations/ai-agent-bridge-to-agent-pontifex.md`](migrations/ai-agent-bridge-to-agent-pontifex.md).
