# R2 fleet admission

Tracking: [program issue #39](https://github.com/ORESoftware/.github/issues/39)
and Linear `DEN-3109`.

This policy separates **collision-safe naming** from **live storage admission**.
A deterministic organization prefix prevents accidental name overlap, but it does
not prove that a bucket exists, that credentials are scoped correctly, that
application authorization is correct, or that retention and key recovery work.

## Authority model

The public contract under `contracts/r2-fleet-admission/` has two independent
authorities:

- TypeSpec; and
- JSON Schema Draft 2020-12.

`ORESoftware/typespec-json-schema-validator` generates JSON Schema from TypeSpec
only as a comparison witness. Generated schema, parity receipts, Contract IR,
runtime types and validator adapters are evidence, never editable authorities.
A missing, stale, partial, unsupported, unauthenticated or zero-step result is not
a pass.

## Physical isolation and names

New buckets use a deterministic organization reservation. One organization may
own several purpose/environment buckets and may use per-customer physical buckets
when the lifecycle and cost model justify them. Every physical bucket must still
have a unique name, state owner and runtime identity.

A per-customer bucket is not the default answer for every object. Use it when an
independent authorization, retention, key-custody, recovery or contractual
boundary warrants the operational cost. Otherwise use an organization-level
bucket with an independently reviewed object-level tenant authorization model.

Never:

- use object-key prefixes as a substitute for an intended physical isolation
  boundary;
- place raw customer identifiers in bucket names;
- interpret a failed or incomplete inventory read as permission to create;
- silently rename, duplicate, import or reassign an existing bucket; or
- derive ownership from a DNS name, repository name or bucket name alone.

## Admission layers

A bucket remains blocked for sensitive documents until every applicable layer
has current evidence:

1. **Namespace:** deterministic organization/customer naming and global collision
   checks.
2. **Inventory:** authenticated account, jurisdiction and resource observation.
3. **State ownership:** one Terraform/OpenTofu state writer and one resource
   address/lineage.
4. **Credential scope:** one least-privilege runtime identity per physical bucket,
   with reader/writer/admin roles separated.
5. **Data plane:** successful own controls plus directed foreign read and write
   denials using nonsensitive canaries.
6. **Application:** Worker, API, admin, signed-URL and direct-S3 authorization,
   including cross-tenant substitution tests.
7. **Cryptography:** accountable key authority, rotation and recovery that does
   not depend solely on the active object credential.
8. **Retention:** object-class policy for versioning, holds, deletion, key horizon
   and export.
9. **Recovery:** byte-identical restore and jurisdiction-safe failover evidence.
10. **Operations:** exact-revision drift checks and sanitized `ores-otel` receipts.

## Public versus private evidence

This public repository records only logical organization names, task links,
coarse evidence states, authority rules and sanitized acceptance criteria.
Provider identifiers and operational evidence remain in approved private stores.

Do not publish:

- Cloudflare account IDs or access-key IDs;
- bucket names, endpoints or object keys;
- customer identifiers or document metadata;
- Terraform state snapshots, backend keys or raw provider payloads;
- secret paths that reveal deployment topology; or
- credentials, private keys, encrypted customer objects or decrypted values.

## Work breakdown

The ordered task ledger is maintained in
[`program.json`](../contracts/r2-fleet-admission/program.json) and issue
[#39](https://github.com/ORESoftware/.github/issues/39). It covers authenticated
inventory, scoped credentials, exact-head CI, TJSV/runtime conformance, legacy
migration, per-customer lifecycle, application authorization, live isolation,
key custody, retention, recovery and nightly evidence.

The first executable gate is restoring exact-head Node/TJSV/OpenTofu execution for
the implementation PR linked from Linear. Until required jobs receive a runner
and produce step-level results, the implementation remains draft and unmerged.

## Change and rollback policy

Changes are pull-request driven and tied to `DEN-3109`. External actions must use
full commit SHAs. Preserve concurrent work, merge rather than rebase, resolve
conflicts semantically, and validate the exact proposed commit.

This policy authorizes no live create, import, apply, move, delete, credential
rotation, token revocation, retention-rule change or customer-data probe. Each
such operation requires its own reviewed task, approved credential channel,
bounded plan and rollback evidence.
