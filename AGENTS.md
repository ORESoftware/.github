<!-- ores-deprecation-routing: 2026-09-01 -->
# DEPRECATION ROUTING

The following ORESoftware repositories are deprecated:

- `ORESoftware/ai-agent-bridge.rs` → `https://github.com/agent-pontifex`
- `ORESoftware/shared-auth-server.rs` → `https://github.com/shared-auth`

Agents must route new feature work to the replacement organization. In a deprecated repository, work is restricted to security remediation, migration support, and narrowly scoped compatibility changes. Do not edit the replacement organization from a legacy-repository task unless that repository is separately named in the task.

# Agent instructions

Before editing:
1. Read repository-local instructions and recent history.
2. Identify the canonical source of truth and downstream consumers.
3. Keep credentials and private data out of prompts, logs, commits, and artifacts.

For conflicts, compare the merge base, both heads, relevant tests, and surrounding commits. Reconstruct intent and produce a coherent combined implementation. Never use blanket ours/theirs resolution for substantive conflicts.

Validate the exact commit being proposed. Do not claim tests or deployments that were not actually run.

## SOPS-managed dotenv repositories

When a repository adopts the ORESoftware SOPS dotenv standard, agents must preserve the exact contract documented in [`docs/sops-environment-standard.md`](docs/sops-environment-standard.md):

- plaintext dotenv files are ignored at every depth;
- the only approved tracked secret-bearing paths are `env/enc/dev.env.enc` and `env/enc/prod.env.enc`;
- decrypted files stay under ignored `env/dec/`;
- root `.env` is absent or a managed relative symlink to `env/dec/dev.env` or `env/dec/prod.env`;
- arbitrary environment names, unexpected `env/enc/*` files, and unmanaged root `.env` replacement are rejected;
- SOPS operations on `.env.enc` files use explicit dotenv input/output types;
- private identities and decrypted values never belong in prompts, Linear, GitHub text, logs, examples, fixtures, caches, or artifacts.

Do not weaken these rules merely to make a test or deployment pass. Record an explicit exception and remediation plan instead.

<!-- ore-org-baseline:begin -->
Read and obey [`agents.md`](agents.md); the lowercase file is canonical.

At minimum: preserve concurrent work; fetch before editing and before pushing; avoid git rebase in favor of git merge; never use `git stash`, `git reset`, `git clean`, `git filter-repo`, force-push, or another destructive operation without exact authorization; resolve conflicts semantically using the merge base, 3–10 relevant commits, tests, contracts, Linear context, and related repositories; never choose `ours` or `theirs` wholesale; scan for conflict markers; validate affected behavior; and never claim remote completion without authoritative evidence.
<!-- ore-org-baseline:end -->
