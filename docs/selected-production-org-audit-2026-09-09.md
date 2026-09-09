# Selected production organization audit — 2026-09-09

Tracking: DEN-3043, DEN-3982, DEN-3440, DEN-3959, DEN-608, DEN-609, DEN-610, DEN-390.

This record captures the evidence-backed state of the requested `ores-cli` production-fleet audit cohort. It is a status and execution backlog, not a claim that inaccessible or uninspected repositories are compliant.

## Cohort and scope

Production organizations in scope:

- `ores-forms`
- `fiducia-cloud`
- `sonus-auris`
- `cliptown`

Organizations whose login ends in `-test` are explicitly out of scope for this cohort.

For each production organization, the audit profile must inspect the organization `.github` repository and the canonical `*-interfaces`, `*-clients`, `*-docs`, and `*-cli` repositories where they exist. It also covers root and relevant nested `.gitignore` files, GitHub Actions workflows, secret-shaped source/config literals, contract-authority boundaries, dependency/release hygiene, and object-store ownership declarations.

Missing access is `inaccessible` or `unknown`; it is never inferred as a pass.

## Current evidence

| Surface | Current evidence | State |
| --- | --- | --- |
| `ORESoftware/ores-cli` installer | PR #39 hardens `oresc`, `ores-cli`, and installed TJSV launchers by resolving chained relative/absolute symlinks before deriving the package root; regression covers a two-hop PATH shim. | proposed / hosted CI admission blocked |
| `ORESoftware/ores-cli` hosted CI | Run `34376564819`, attempt 3, job `102562751140` received no runner (`runner_id: 0`) and executed zero steps. | infrastructure admission failure; not a source-test result |
| `cliptown/cliptown-interfaces` | PR #30 merged after the TJSV lane reached 4 declarations, 231 probes, 231 agreements, zero findings/divergences/refusals and the complementary parity generator was brought current. | merged |
| `fiducia-cloud/fiducia-infra` R2 delegation | `scripts/r2-scoped-creds.sh` mints short-lived credentials for exactly one caller-supplied bucket, but currently accepts any nonempty bucket name. Existing regression uses `fiducia-logs-prod`. | namespace validation missing; DEN-608 reopened |
| TJSV Action production dependencies | During Cliptown certification, `npm ci --omit=dev` reported three high-severity vulnerabilities even though contract comparison later passed. | dependency-health task recorded on DEN-3959 |
| `ores-forms` | The current connected GitHub installation cannot resolve `ores-forms/.github`. | inaccessible; no compliance claim |

## Required `ores-cli` audit rules

### Repository-family coverage

For every selected production organization, enumerate the exact default-branch revisions of `.github`, `*-interfaces`, `*-clients`, `*-docs`, and `*-cli`. Record absent repositories separately from inaccessible repositories. Do not substitute similarly named `*-test` repositories.

### Git and ignore hygiene

Audit root and relevant nested `.gitignore` files for at least:

- `.env` / environment-specific plaintext while preserving reviewed examples;
- decrypted SOPS material under the approved `env/dec/` layout;
- age identity/private-key material;
- `tmp/`, `temp/`, scratch, local worktree, cache, coverage, and build output;
- validator/generated evidence that is intentionally ephemeral rather than reviewed source.

A missing ignore is a finding; an ignored file is not proof that historical or tracked secrets do not exist.

### GitHub Actions hardening

Flag at least:

- mutable action tags instead of immutable full commit SHAs;
- `ubuntu-latest` or other moving runner labels where a tested exact image is required;
- mutable runtime/tool versions such as `stable`, broad Node majors, or floating `npx` installs;
- checkout with persisted credentials when not explicitly required;
- overbroad workflow/job permissions;
- absent timeouts or inappropriate absence of concurrency cancellation;
- unsafe shell interpolation, `eval`, command reconstruction, or secret-bearing argv/URLs;
- skipped/missing/zero-step jobs represented as success;
- executed red jobs versus pre-step admission failures as separate evidence classes.

### Secret scanning

Scan source, configuration, documentation, and workflow text for secret-shaped literals and known unsafe credential channels. Findings and receipts must redact values. Example placeholders must not be misclassified as live credentials merely because their variable names contain `TOKEN`, `KEY`, or `SECRET`.

### Contract authority and TJSV

Where a repository owns cross-language contracts:

- independently authored TypeSpec and independently authored JSON Schema Draft 2020-12/OpenAPI remain peer top-level authorities;
- TypeSpec-generated JSON Schema, Contract IR, generated interfaces/clients, projection receipts, and runtime evidence remain downstream witnesses only;
- `ORESoftware/typespec-json-schema-validator` is pinned to an immutable reviewed revision and must stop on unexplained structural, differential, declaration-scope, or projection/runtime divergence;
- a repository without an independent peer authority must be reported as `missing-peer` rather than creating a fake generated second authority solely to satisfy a gate.

### R2 namespace and isolation

R2 bucket ownership needs a machine-checkable fleet contract. The desired shape must allow both organization-purpose buckets and many per-customer buckets while remaining globally collision-resistant, for example:

```text
<org-prefix>-<purpose>-<environment>
<org-prefix>-customer-<stable-customer-id>-<purpose>-<environment>
```

The exact grammar must enforce provider character/length constraints, normalization rules, reserved organization prefixes, and collision detection. Object-key prefixes alone are not an organization/customer security boundary; credentials should remain bucket-scoped or narrower.

Existing bucket names must first be inventoried read-only. Any production rename or migration is a separate reviewed roll-forward; the audit must never auto-delete or purge a bucket.

## Linear routing

The following work is already represented and must be updated rather than duplicated:

- DEN-3043 — fleet linter and machine-readable audit receipts;
- DEN-3982 — recurring fleet cross-check adoption;
- DEN-3440 — zero-step GitHub Actions admission classification;
- DEN-3959 — peer TypeSpec/JSON Schema convergence and temporary ownership of the newly observed TJSV dependency-advisory task;
- DEN-608 — reopened for Fiducia R2 bucket namespace enforcement;
- DEN-609 — Sonus Auris audit umbrella with existing bounded CI/security/release owners;
- DEN-610 — Cliptown audit umbrella; interface hardening PR #30 is merged;
- DEN-390 — `ores-cli` / flags-2-env installer and contract-audit hardening.

A dedicated fleet-R2 naming issue was attempted on September 9 and Linear rejected it because the workspace has exceeded its issue-count limit. Until capacity exists, DEN-608 owns the concrete Fiducia implementation and DEN-3043 owns the cross-fleet lint rule. No fabricated Linear identifier is used.

## Next implementation slices

1. **Fiducia R2** — add fail-closed organization-prefix/per-customer bucket-name validation and adversarial tests before the temporary-credential request is made; then expose the rule through `ores-cli` without duplicating the grammar.
2. **Fiducia interface CI** — reconcile the older Python/jsonschema `interface-schemas` workflow with the already stronger pinned TJSV authority lane; remove redundancy only when semantic coverage is preserved.
3. **Sonus interfaces** — pin moving runners/actions/toolchains and establish the missing independent peer-authority migration path under existing Sonus tickets; do not manufacture a generated JSON Schema authority.
4. **Ores CLI installation** — finish exact-source verification for PR #39, including symlink loops and PATH-shim variants, while DEN-3440 owns the hosted zero-step runner problem.
5. **TJSV supply chain** — identify and remediate the three high-severity production advisories and add a deterministic high-or-higher production dependency gate.
6. **Ores Forms** — rerun the exact same audit only after the GitHub installation exposes the production org; retain `inaccessible` until then.

## Completion rule

This audit cohort is complete only when every selected organization has an exact inventory receipt, every accessible target repository has an evidence-backed result for the requested checks, all unexplained contract or secret findings are routed to an owner, R2 ownership collisions are fail-closed, and inaccessible surfaces remain explicitly unresolved rather than inferred green.
