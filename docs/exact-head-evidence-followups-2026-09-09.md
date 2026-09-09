# Exact-head evidence follow-ups — 2026-09-09

Tracking controller: Linear `DEN-268`.

This document records the next residual tasks discovered after reconciling the current exact-head CI/PR evidence backlog against existing Linear and GitHub ownership. It intentionally does **not** duplicate the existing dispatcher, zero-step classifier, evidence-expiry controller, exact-head reviewer, stale-narrative task, or canary receipt work.

## Discovery basis

The current backlog already distinguishes these live evidence classes:

- no required workflow run exists for the exact head;
- a run/job exists but executes zero steps;
- code actually executes and fails;
- an approved credential boundary prevents a private dependency from being reached;
- deterministic generated evidence drifts from authority/source;
- PR narrative assertions drift from the current head;
- previously valid evidence expires after subject or policy drift.

Existing ownership remains:

- `DEN-268` — cross-portfolio execution controller;
- `DEN-3440` — pre-admission / zero-step classification;
- `DEN-2776` — residual GitHub Actions and branch-policy reconciliation;
- `DEN-3435` — stale evidence invalidation / recertification;
- `DEN-3776` — exact-head PR reviewer;
- `DEN-3779` — bounded Actions dispatch/offload;
- `.github#44` — machine-readable canary receipt / promotion blocker;
- `.github#94` — exact-head Actions scheduling after GitHub App/API writes;
- `.github#98` — stale PR narrative detection.

The residual gaps are therefore a **shared state vocabulary** across those components and a **capacity-recovery reconciliation path** for GitHub-only tasks.

## New task 1 — `.github#127`: version the fleet evidence-state contract

Issue: <https://github.com/ORESoftware/.github/issues/127>

### Goal

Define one versioned, machine-readable classification boundary shared by fleet scanners, dashboards, exact-head review, bounded-dispatch receipts, `ores-cli`, and promotion gates.

### Minimum states

The contract must keep these states semantically distinct:

- `missing_exact_head_run`
- `pre_admission_zero_step`
- `executed_code_failure`
- `credential_boundary`
- `deterministic_artifact_drift`
- `stale_pr_narrative`
- `stale_evidence`
- `scheduled`
- `running`
- `passed`
- `unverifiable`

A producer may expose more detail, but downstream consumers must not collapse materially different states into one generic red/green result.

### Required evidence binding

Every classification should be explainable from preserved raw facts and bind, where applicable, to:

- repository and PR/ref;
- base SHA / base policy context;
- exact head or promotion candidate SHA;
- workflow/check/policy identity;
- run/job/attempt/receipt identifiers;
- evidence timestamps and freshness/expiry inputs;
- classifier/schema version.

Zero steps or `runner_id = 0` never proves billing by itself. Billing is a specific diagnosis that requires explicit billing/spending evidence.

### Regression witnesses

Keep public/redacted fixtures for the current canaries without embedding credentials or private payloads:

- `fiducia-cloud/fiducia-clients#105` — missing exact-head run;
- `ORESoftware/ores-cli#39` — pre-admission zero-step;
- `ORESoftware/ores-cli#40` — stale PR assertion;
- existing deterministic-artifact-drift witnesses;
- existing stale-evidence / recertification fixtures from DEN-3435.

### Integration rule

This task defines the shared vocabulary, schema, compatibility, and consumer boundary. It does **not** replace DEN-3440, DEN-3435, DEN-3776, DEN-3779, or `.github#44`; those components should emit or consume the common contract instead of growing incompatible parallel taxonomies.

## New task 2 — `.github#130`: reconcile GitHub-only tasks after Linear capacity recovery

Issue: <https://github.com/ORESoftware/.github/issues/130>

### Problem

On 2026-09-09, a real attempt to create a dedicated Linear issue for `.github#127` was rejected because the workspace had exceeded its free issue-count limit. The existing safe fallback is a GitHub executable task plus a link/comment on an existing Linear controller. That fallback needs an explicit recovery path so it does not become permanent drift.

### Required inventory

Maintain a machine-readable capacity-fallback record containing at minimum:

- GitHub repository + issue number;
- stable task fingerprint;
- intended Linear workspace/team/project;
- temporary Linear controller, if any;
- source/discovery provenance;
- creation timestamp;
- current disposition (`actionable`, `completed`, `duplicate`, `superseded`, `absorbed`, `blocked`, or `unverifiable`);
- eventual Linear issue identifier only after Linear actually assigns one.

Never invent a `DEN-*` identifier.

### Reconciliation behavior

When issue capacity is genuinely available:

1. Read the inventory; do not create throwaway probe issues.
2. Search Linear and GitHub for matching fingerprints, titles, source links, and existing DEN references.
3. Classify each item before mutation.
4. Create at most one dedicated Linear issue for each still-actionable GitHub-only task that has no existing owner.
5. Add reciprocal links/comments and persist the real assigned DEN identifier.
6. Preserve GitHub issue/comment history; do not delete the fallback task after backfill.
7. Make repeated runs idempotent and safe if capacity disappears again mid-run.

Initial inventory includes at least `.github#94`, `.github#98`, `.github#127`, and the TJSV rollout tasks that carry the same verified capacity-fallback note after de-duplication.

## Linear status

A dedicated Linear issue for the evidence-state contract was attempted on 2026-09-09 and Linear returned a workspace issue-limit error. No fake DEN identifier was created.

Until capacity returns:

- `.github#127` and `.github#130` are the executable task records;
- `DEN-268` is their Linear-side coordination controller;
- project-specific controllers continue to own their existing capacity-fallback tasks;
- no automation should repeatedly probe the limit by creating throwaway Linear issues.

## Execution order

1. **`.github#127` first** — stabilize the shared evidence-state vocabulary and compatibility rules.
2. **`.github#94` + DEN-3440** — emit the shared states for missing exact-head workflows versus pre-admission zero-step jobs.
3. **`.github#98` + DEN-3776 + DEN-3435** — emit the same contract for stale narrative and stale evidence.
4. **Fleet scanner / dashboard / merge gates** — consume the shared schema and fail closed on unknown or unverifiable evidence.
5. **`.github#130`** — maintain the capacity-fallback inventory now; perform dedicated Linear backfill only when issue capacity is actually available.

## Completion standard

Documentation and issue creation are planning evidence, not implementation completion. A task is complete only when its owning implementation is exact-head tested, remote evidence is durable, downstream consumers are updated without duplicate taxonomies, and the relevant Linear/GitHub records accurately reflect the final state.
