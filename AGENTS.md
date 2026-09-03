# Agent instructions

Before editing:
1. Read repository-local instructions and recent history.
2. Identify the canonical source of truth and downstream consumers.
3. Keep credentials and private data out of prompts, logs, commits, and artifacts.

For conflicts, compare the merge base, both heads, relevant tests, and surrounding commits. Reconstruct intent and produce a coherent combined implementation. Never use blanket ours/theirs resolution for substantive conflicts.

Validate the exact commit being proposed. Do not claim tests or deployments that were not actually run.

## SOPS-managed dotenv repositories

When a repository adopts the ORESoftware SOPS dotenv standard, preserve the
exact contract in [`docs/sops-environment-standard.md`](docs/sops-environment-standard.md):

- required ciphertext paths are `env/enc/dev.env.enc` and `env/enc/prod.env.enc`;
- `env/enc/stage.env.enc` is the only optional exact third environment;
- plaintext stays only under ignored `env/dec/{dev,stage,prod}.env`;
- root `.env` is absent or a managed relative symlink to one configured target;
- `staging`, `qa`, wildcard rules, arbitrary names, and unexpected `env/enc/*` files are rejected;
- access is per ciphertext recipient list, not repository membership;
- stage-enabled policies retain a true dev-only recipient omitted from stage and prod;
- use `--require-stage-exclusive` when stage recipients must be omitted from prod and `--require-prod-exclusive` when a production-only identity is required;
- `.sops.yaml` edits are incomplete until affected ciphertext metadata is synchronized with `ores-sops sync-keys <environment>` or `sops updatekeys`;
- SOPS operations on `.env.enc` use explicit dotenv input/output types;
- private identities and decrypted values never belong in prompts, Linear, GitHub text, logs, examples, fixtures, caches, or artifacts;
- run `ores-sops verify` and the required ciphertext access audit; never use `--policy-only` after ciphertext exists.

Do not weaken these rules merely to make a test or deployment pass. Record an explicit exception and remediation plan instead.

<!-- ore-org-baseline:begin -->
Read and obey [`agents.md`](agents.md); the lowercase file is canonical.

At minimum: preserve concurrent work; fetch before editing and before pushing; avoid git rebase in favor of git merge; never use `git stash`, `git reset`, `git clean`, `git filter-repo`, force-push, or another destructive operation without exact authorization; resolve conflicts semantically using the merge base, 3–10 relevant commits, tests, contracts, Linear context, and related repositories; never choose `ours` or `theirs` wholesale; scan for conflict markers; validate affected behavior; and never claim remote completion without authoritative evidence.
<!-- ore-org-baseline:end -->
