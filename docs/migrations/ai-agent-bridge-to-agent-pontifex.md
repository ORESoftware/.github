# Migrate `ORESoftware/ai-agent-bridge.rs` to Agent Pontifex

Decision date: 2026-09-03

## Canonical destination

New agent-bridge development belongs in
[`agent-pontifex/ai-agent-bridge.rs`](https://github.com/agent-pontifex/ai-agent-bridge.rs).
The broader successor organization also owns the coordinator and SDK surfaces;
the exact bridge repository is the canonical replacement recorded in
`deprecated-repositories.json`.

## Evidence supporting deprecation

- The canonical bridge repository exists under the `agent-pontifex`
  organization and exposes the active HTTP, SSE, TCP, topic-routing, shared
  context, and repository-lease implementation.
- `ORESoftware/ai-agent-bridge.rs` now begins both `README.md` and `AGENTS.md`
  with an Agent Pontifex migration notice.
- Its permanent `Deprecation guard` workflow fails when either notice stops
  being first or stops naming the successor.
- The historical repository has no authority for new features, releases, or
  deployments. Its permitted work is limited to deprecation maintenance,
  security remediation, migration, narrow compatibility, and historical
  reference.

## Consumer migration gate

Do not redirect a consumer solely by changing a Git URL. For each consumer:

1. Record the exact legacy revision and the exact Agent Pontifex revision.
2. Compare package names, enabled Cargo features, configuration keys,
   transports, authentication behavior, persistence behavior, and protocol
   surfaces used by that consumer.
3. Run the consumer's locked build, tests, and an end-to-end bridge handshake
   against the exact replacement revision.
4. Move dependency orchestration to the owning package graph where applicable,
   then record the immutable resolution.
5. Remove the legacy dependency only after equivalent behavior is proven.
6. Roll back by restoring the recorded legacy revision if the exact replacement
   fails the consumer's canary.

This deprecation is therefore a routing and release-authority decision, not a
claim that every downstream consumer has already migrated.
