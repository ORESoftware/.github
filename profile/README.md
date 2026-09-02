<!-- ores-deprecated-repositories: 2026-09-01 -->
> [!IMPORTANT]
> **Deprecated ORESoftware repositories**
>
> - [`ORESoftware/ai-agent-bridge.rs`](https://github.com/ORESoftware/ai-agent-bridge.rs) is superseded by [`agent-pontifex`](https://github.com/agent-pontifex).
> - [`ORESoftware/shared-auth-server.rs`](https://github.com/ORESoftware/shared-auth-server.rs) is superseded by [`shared-auth`](https://github.com/shared-auth).
>
> New feature development belongs in the replacement organizations. The legacy repositories are limited to security, migration, and narrowly scoped compatibility work.

# ORESoftware

This organization maintains software, infrastructure, interfaces, clients, services, and supporting documentation under a shared engineering baseline.

## Working principles

- Keep changes reviewable, tested, and reversible.
- Treat security, privacy, compatibility, and data durability as design constraints.
- Resolve merge conflicts semantically: reconstruct both sides' intent, preserve compatible behavior, and document deliberate trade-offs.
- Prefer canonical repositories and short, stable names; deprecate duplicates with migration notes rather than silently deleting history.
- Keep cross-repository dependencies explicit and pinned where reproducibility matters.

Organization-wide contribution and security guidance lives in this `.github` repository.

<!-- ore-org-baseline:begin -->
This GitHub account maintains software, infrastructure, research, and supporting documentation under the [`ORESoftware`](https://github.com/ORESoftware) GitHub owner.

Planning and delivery context is tracked in [github.com/ORESoftware](https://linear.app/denman/project/githubcomoresoftware-1574ce77fadf). Public contribution, security, and governance defaults are maintained in [`.github`](https://github.com/ORESoftware/.github).

Repository descriptions and repository-local documentation remain authoritative for each project. Do not infer production readiness, support commitments, or security guarantees from this profile alone.
<!-- ore-org-baseline:end -->
