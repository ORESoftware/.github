# Account-level `.github` agent instructions

<!-- ore-org-baseline:begin -->
These instructions apply to this repository. Repository-local instructions may add stricter requirements, but they must not weaken this baseline.

## Discover instructions hierarchically

Resolve the current working directory, walk upward to the filesystem root, and read every readable **lowercase** `agents.md` on that ancestor chain in root-to-leaf order. Do not search sibling directories. Report unreadable instruction files rather than silently ignoring them.

Lowercase `agents.md` is canonical. Uppercase or provider-specific files are compatibility mirrors and must direct the agent back to the applicable lowercase file.

## Inspect and synchronize before editing

Before changing files, inspect the current branch, complete working tree, remotes, default branch, open pull requests, linked GitHub issues, linked Linear work, repository-local documentation, and relevant related repositories.

Use non-destructive inspection and synchronize remote knowledge before making decisions:

```sh
git status --short --branch
git remote -v
git fetch --all --prune
```

Preserve every uncommitted user or agent change. Never treat unfamiliar work as disposable. Before pushing, fetch again, incorporate the current remote branch and default branch, and **avoid git rebase in favor of git merge.** Push a feature branch and use a pull request unless the repository is being initialized from an otherwise empty bootstrap commit.

## Mandatory semantic conflict resolution

> resolve any and all git conflicts semantically, will full context, even looking back 3-10 commits in git log history for more context - never hastily pick sides in a conflict but merge things conceptually, using max context and complete conceptual awareness for a given github organization's repos and external org repos too

For every conflict:

1. Read the merge base, both sides, surrounding implementation, tests, schemas, generated artifacts, documentation, deployment configuration, and public API contracts.
2. Inspect the affected path history and normally review 3–10 relevant commits on each side using `git log`, `git show`, and `git blame` where useful.
3. Review linked pull requests, issues, Linear work, and related repositories in this organization and external organizations whenever behavior or contracts cross repository boundaries.
4. Preserve compatible intent and invariants from both sides. Synthesize a conceptual merge; never resolve merely by selecting `ours`, `theirs`, `current`, or `incoming` wholesale.
5. Scan the complete worktree for unresolved markers:

   ```sh
   git grep -n -E '^(<<<<<<<|=======|>>>>>>>)' -- .
   ```

6. Run the smallest relevant checks while iterating, then the complete applicable formatter, linter, unit, integration, contract, build, and end-to-end gates.
7. Document incompatible requirements, intentional behavioral choices, and discarded intent in the commit or pull-request description.

## Destructive operations are default-deny

Do not run or recommend destructive or history-rewriting operations unless the user explicitly authorizes that **exact operation for the exact paths or refs** after the impact has been explained. The blacklist includes, but is not limited to:

- `git stash` in any form;
- `git reset` in any mode;
- `git clean` in any mode;
- `git rebase` and interactive history rewriting;
- `git filter-repo`, `git filter-branch`, BFG, or equivalent repository-history rewrites;
- `git push --force` or `--force-with-lease`;
- `git branch -D`, forced checkout, destructive `git restore`, or discarding worktree/index changes;
- amending or replacing shared commits;
- deleting or moving worktrees, submodules, branches, tags, repositories, releases, packages, environments, secrets, databases, buckets, clusters, namespaces, or infrastructure state;
- shell-level destructive edits such as recursive `rm`, `find -delete`, truncation, shredding, or broad in-place replacement over unreviewed paths;
- bypassing hooks, review, branch protection, required checks, policy gates, or audit logging.

Do not use destructive commands merely to make tests pass or to simplify a merge. Prefer additive edits, patch-based changes, new branches, explicit copies, and reversible migrations.

## Source ownership, generated files, worktrees, and submodules

Edit the authoritative source repository, not a generated mirror, vendored copy, build output, deployment artifact, package cache, or downstream consumer. Identify generators and regenerate derived artifacts from reviewed sources. Never detach, relocate, absorb, remove, or rewrite a submodule or worktree without explicit authorization and full cross-repository context.

## Secrets and sensitive data

Never commit, print, log, paste into prompts, or place in fixtures any token, password, private key, session secret, database URL, customer data, legal record, private health data, or unpublished security detail. Use documented secret stores and redacted examples. If a credential is exposed, stop using it, remove it from active artifacts where safely possible, revoke or rotate it, and document the incident through an approved private channel. History rewriting still requires exact authorization.

## SOPS-managed application dotenv

Repositories adopting the ORESoftware SOPS dotenv standard must follow
[`docs/sops-environment-standard.md`](docs/sops-environment-standard.md).

- Required exact ciphertext paths are `env/enc/dev.env.enc` and
  `env/enc/prod.env.enc`.
- `env/enc/stage.env.enc` is the only optional exact third environment.
- Plaintext stays under ignored `env/dec/{dev,stage,prod}.env`; root `.env` may
  only be a managed relative symlink to one configured target.
- Reject `staging`, `qa`, wildcard rules, arbitrary names, and unexpected
  `env/enc/*` files.
- Repository read access exposes ciphertext, not plaintext. Decryption rights
  come from the exact per-file age/KMS recipient set.
- A stage-enabled matrix must retain at least one true dev-only recipient absent
  from stage and prod. Enforce stage-not-prod and prod-only boundaries where the
  repository policy requires them.
- Never copy every recipient into every environment merely to make automation
  pass.
- A recipient change is incomplete until the affected ciphertext is synchronized
  with `ores-sops sync-keys <environment>` or `sops updatekeys` and the
  desired-versus-actual access audit passes.
- `--policy-only` is bootstrap-only and must not be used to bypass existing
  ciphertext checks.
- Never expose decryption identities to fork-originated pull requests.
- Once plaintext exists, local OS permissions apply; do not share one OS account
  between privileged and unprivileged developers, and normally materialize
  production plaintext only on protected deployment workloads.

## Pull requests, tests, and evidence

Use focused commits and draft pull requests. Link the relevant Linear project or issue. Explain behavior, risks, migration and rollback considerations, security impact, tests run, and any cross-repository dependencies. Pin external GitHub Actions to full commit SHAs; declare least-privilege workflow permissions, explicit timeouts, concurrency cancellation where appropriate, and `persist-credentials: false` for checkout.

Never report a branch, commit, pull request, merge, deployment, test run, or external update as completed without authoritative remote evidence. Local files and generated archives are not a substitute for a pushed repository and verifiable GitHub state.
<!-- ore-org-baseline:end -->

## Red PRs, stale PRs, and mandatory cherry-pick

Superseded PRs often still contain ideas we want. Follow [`docs/stale-and-red-pull-requests.md`](docs/stale-and-red-pull-requests.md) on every org we own:

- Diagnose red CI from the job log and try to get the PR green (merge main in; do not rebase).
- If the PR is stale or outmoded, comment with salvage links and **cherry-pick** unique tests, contracts, hardening, and docs. Do not close it unless a human asked.
- Do not rebase, stash, reset, or force-push unless a human named that exact operation.
