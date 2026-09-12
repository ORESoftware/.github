# Organization source-of-truth governance

This directory defines the machine-readable organization contract used to reconcile the ORESoftware control surfaces.

## Authority

`governance/source-of-truth.toml` in the owner-level `.github` repository is the canonical organization manifest. The manifest is intentionally separate from long-form prose: it identifies the repositories and external resources that carry the product and operating direction, while the linked repositories and systems retain their own detailed material.

The following surfaces must agree with the canonical manifest:

- the active `*-docs` repository;
- the Astro `<owner>.github.io` marketing repository;
- the owner-level `*-mcp-server.rs` repository;
- the owner-level CLI repository when a CLI is declared;
- the Linear project and its documents;
- the primary GitHub Project and tracked issues;
- the Supabase organization or approved shared namespace, Neon organization, Cloudflare domain, GCP project, and Slack channel.

## Append-only reconciliation

Direction changes do not erase history.

1. Add a `[[supersessions]]` entry describing the former statement, the replacement, the reason, the evidence link, and the timestamp.
2. Update the current manifest fields in the same reviewed change.
3. Preserve the old prose in its existing Git history and, where a marketing page changes visible copy, retain the superseded copy in a non-interactive historical element or linked changelog rather than silently deleting it.
4. Update mirrors with the canonical revision/digest. A mirror may contain the full normalized manifest or a pointer record; it must not create a competing authority.
5. Do not copy credentials, tokens, private keys, connection strings, one-time codes, or sensitive personal data into this file.

## Independent contract authorities

`source-of-truth.tsp` and `source-of-truth.schema.json` are independently authored top-level contracts. TypeSpec may generate JSON Schema B, while the hand-authored JSON Schema is JSON Schema A. The `tjsv` validator compares normalized top-level declarations and validates generated artifacts without treating either source as subordinate.

A change is incomplete when only one contract is updated. Contract parity, the example TOML instance, and repository-specific fixtures must all pass before merge.

## Status vocabulary

Every repository and external mapping records one status:

- `verified`: observed through the relevant connected system and consistent with the contract;
- `declared`: intentionally selected but not yet independently observed;
- `drift`: observed but inconsistent with the expected value;
- `missing`: the expected resource was checked and does not exist or is not visible;
- `blocked`: a prerequisite or administrative action prevents completion;
- `unverified`: not checked with an authoritative connector during the recorded review.

Audits must not convert `declared`, `blocked`, or `unverified` into `verified` merely because the identifier looks plausible.

## Read-only audit and explicit mutation

The `ores-cli`/`oresc` alignment audit is read-only. It inventories repositories, loads the canonical manifest, checks normalized mirror data, and writes findings to stdout. Repository creation, visibility changes, document updates, issue creation, and other mutations remain separate explicit operations and must produce reviewable commits or receipts.

## Validation targets

At minimum, fixtures cover:

- exact canonical/mirror agreement;
- stale mirror revision or digest;
- missing required surface;
- malformed owner-qualified repository name or URL;
- organization mismatch;
- expected-private canonical repository observed as public;
- absent optional CLI;
- external mapping declared but unverified;
- append-only supersession order and duplicate revision detection.
