# Linear and GitHub operating model

This is the fleet-wide contract for turning ChatGPT requests, Linear planning, GitHub issues, pull requests, Projects, and deployments into one auditable workflow.

## Sources of truth

- **GitHub** is authoritative for repositories, code, branches, commits, pull requests, checks, releases, deployment manifests, and technical landing evidence.
- **Linear** is authoritative for planning scope, ownership, priority, dependencies, acceptance criteria, and portfolio status.
- **GitHub Projects** provide the organization-level execution view. Each organization normally uses Project #1 titled `<canonical-org-login>-project`; registry overrides are explicit.
- **Organization `.github` repositories** hold public routing, contribution, security, support, and agent guidance shared across the organization.

## Intake and de-duplication

1. Normalize each actionable request into concrete deliverables, owners, repositories, and acceptance criteria.
2. Search GitHub default branches, feature branches, pull requests, issues, releases, and Linear before mutation.
3. Reuse or amend exactly one canonical Linear issue when residual scope remains.
4. Create a new issue only when no existing issue safely owns the work. A similar title alone is not sufficient evidence either way.
5. Preserve completed and duplicate/reference-only issues; do not reopen them without new contradictory evidence.
6. Record source fingerprints and bounded summaries, not hidden reasoning, credential values, or unnecessary private content.

## Git and pull-request contract

- Use a Linear-linked branch such as `alexanderdmills/den-834-...` or another deterministic branch that contains the issue identifier.
- Include the Linear identifier in the commit subject and PR title or body.
- Link the canonical GitHub issue with `Closes`, `Fixes`, or `Resolves` when one exists.
- Keep each PR bounded to one coherent acceptance slice.
- Rebase or merge the latest base branch semantically. Preserve independent intent from both sides; never resolve conflicts by blindly selecting `ours` or `theirs`.
- Run focused tests and required repository checks. A green focused test does not override a red required shared gate.
- Merge only when the final head is reviewable, required checks pass or an explicit reviewed policy exemption applies, no unresolved review thread remains, and the merge is not superseded by a newer carrier.
- **Red and stale PRs:** try to make red PRs green. When a PR is outmoded, comment and cherry-pick unique work; never discard the branch without salvage. See [`stale-and-red-pull-requests.md`](./stale-and-red-pull-requests.md). Do not rebase, stash, reset, or force-push unless a human named that exact operation.

## Status transitions

- **Backlog/Todo:** accepted work, not actively executing.
- **In Progress:** implementation or evidence collection is active.
- **Integration complete:** code is merged to an integration branch, but production delivery remains open.
- **Done:** acceptance evidence is on the default branch and any required deployment, release, live canary, operator action, or audit evidence is complete.
- **Duplicate:** unique scope has been transferred to the canonical issue and a real duplicate relationship is recorded.

Do not mark security rotation, repository creation, secret provisioning, deployment, or live verification complete from a chat claim alone.

## Organization routing

The canonical registry is [`github-linear-project-registry.md`](./github-linear-project-registry.md), backed by the version-controlled TSV in `ORESoftware/k8s-cluster`.

For each organization:

1. keep one active canonical GitHub Project;
2. keep one public `.github` repository;
3. publish the Linear and Project routing block without overwriting unrelated prose;
4. keep one durable governance issue in the Project;
5. attach exact PR, merge, workflow, release, or deployment evidence to the owning Linear issue.

## Authentication and secret safety

- Prefer GitHub App installation tokens with the minimum owner/repository permissions and short lifetime.
- Never put a PAT, private key, bearer token, password, database URL credential, or cloud key in chat, Linear text, GitHub issue/PR text, commits, workflow inputs, logs, artifacts, shell arguments, or Git remotes.
- A credential pasted into any of those surfaces is exposed even when the user intended to authorize its use. Revoke it and record only redacted incident metadata.
- Repository creation and organization administration must use a separately scoped GitHub App or protected operator path; read-only CI credentials must not be reused for administration.
- Importers and prompt-intake agents must fail closed, quarantine sensitive content, and retain only non-sensitive source identity needed for audit and idempotency.

## Recurring reconciliation

The prompt-intake workflow under DEN-834 and the project/document reconciler under DEN-2242 must be idempotent. Each run publishes:

- the window and durable run identity;
- scanned/actionable/excluded counts;
- existing issue matches, creates, amendments, and duplicate collapses;
- exact GitHub landing evidence;
- ambiguous or externally blocked items;
- a redacted failure summary and rerun instructions.

A rerun over the same source window must create zero duplicate issues, comments, repositories, Projects, or PRs.
