# Deprecated ORESoftware repositories

`deprecated-repositories.json` is the machine-readable authority for repositories
that have moved out of the `ORESoftware` owner. A deprecated repository remains
available only to preserve links and migration history. It must not publish,
deploy, receive feature work, or become a dependency source again.

| Historical repository | Canonical repository | Release authority |
|---|---|---|
| `ORESoftware/shared-auth-server.rs` | `shared-auth/shared-auth-server.rs` | Canonical repository only |

Every listed historical repository must prepend its README and repository-local
agent instructions with the canonical destination, keep package publication
disabled, and carry a fail-closed test that rejects release/deployment
capabilities. New entries require evidence that the destination is operational
and contains the authoritative history or an explicit migration plan.
