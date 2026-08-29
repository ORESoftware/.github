# Red PRs, stale PRs, and mandatory cherry-pick

This is the fleet rule for **every GitHub org we own** (product orgs, sibling `*-test` orgs, and the `ORESoftware` user namespace). It exists so superseded pull requests still donate unique tests, contracts, and hardening instead of disappearing.

Linear: [DEN-1906](https://linear.app/denman/issue/DEN-1906)  
GitHub: [ORESoftware/.github#18](https://github.com/ORESoftware/.github/issues/18)

Google Chat source keys (no bodies):

- `google-chat:AAQAoHKdzvI:spaces/AAQAoHKdzvI/messages/xLnZ3YGXv6U.xLnZ3YGXv6U`
- `google-chat:AAQAoHKdzvI:spaces/AAQAoHKdzvI/messages/I5lDvl6D69s.I5lDvl6D69s`
- `google-chat:AAQAoHKdzvI:spaces/AAQAoHKdzvI/messages/TKKcJjkOpuc.TKKcJjkOpuc`

## Try to make red PRs green

A PR is red when its latest commit status rollup is `FAILURE` or `ERROR`, or required checks failed.

1. Diagnose from the job log, not from the title.
2. Real test / type / lint / contract failure: **fix the PR**. Merge `origin/main` into the PR branch with a merge commit, not rebase. Resolve conflicts semantically with at least 5 commits of history. Push. Re-run checks.
3. Merge conflict / `DIRTY`: **merge main in**. Do not rebase, stash, or reset.
4. GitHub Actions minutes exhausted / jobs dying in a few seconds with no steps: cannot code-fix to green. Comment that the check is budget-blocked and move unique work to a salvage PR or a `*-test` org that still has minutes.
5. Dependabot bump with red CI: update the bump against current `main` if the dependency is still wanted; otherwise salvage any accompanying lockfile / workflow pin that is still correct.
6. Push the fix to the existing PR branch when it is still the right vehicle. Open a new PR only when the old one is the wrong vehicle (wrong base, superseded product direction, or abandoned author path).
7. Sibling `*-test` orgs exist in part so we can spend GHA minutes there when the product org is on budget.

## Old / outmoded / redundant PRs: comment, do not throw the work away

A PR may be treated as stale (comment instead of driving it to merge) when a human has said it is obsolete, or when **all** of the following are true:

- it is clearly superseded (same change already on `main`, or a newer PR covers the same intent), **or**
- it is months stale with no unique product direction left, **or**
- it is a duplicate fleet campaign (identical title across many repos) whose unique hunks have already been harvested.

Then:

1. **Comment on the original PR** explaining why it is not being driven to green, and **link every salvage commit / salvage PR**. Do not close it unless a human asked to close it.
2. **Cherry-pick is mandatory.** Read the full PR diff and at least 5 commits of history on both the PR branch and `main`. Harvest, at minimum:
   - tests, contracts, JSON Schema, FORCE RLS, fail-closed parsers, and typed-error paths
   - hardening (CSP, query allowlists, digest-only storage, no secrets in fixtures)
   - unique docs, Linear/ticket links, and workflow pins that `main` still lacks
   - generated artifacts that match current generators (re-run generate rather than copying stale generated files blindly)
3. Apply salvage with `git cherry-pick` (or a merge commit of a salvage branch). **Do not rebase. Do not stash. Do not reset.** If a cherry-pick conflicts, resolve semantically — not by picking one side.
4. Empty, secret-bearing, or provider-UI-automation hunks are the exception: do not salvage those; say so in the comment.
5. Duplicate fleet titles still need a per-repo skim: one repo may have a real unique fix hiding under a copy-pasted title.

## What not to do

- Do not close or ignore a red PR because CI is red without reading the diff.
- Do not drop a stale PR's unique tests or hardening because the rest of the PR is obsolete.
- Do not rebase the stale branch onto main "to make cherry-pick easier."
- Do not force-push, and do not skip hooks, unless a human explicitly asked.
