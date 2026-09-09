# R2 fleet admission contract

Tracking: [ORESoftware/.github#39](https://github.com/ORESoftware/.github/issues/39) and Linear `DEN-3109`.

`main.tsp` and `authored.schema.json` are independent, human-maintained peer
authorities. Neither is generated from, ranked beneath, or automatically repaired
from the other. The TypeSpec-generated JSON Schema is a comparison witness only.

The exact-commit-pinned `ORESoftware/typespec-json-schema-validator` workflow must:

1. inventory the TypeSpec declarations;
2. generate comparison-only JSON Schema from TypeSpec;
3. validate both schema lanes;
4. compare top-level identities and recursive semantics;
5. run both validators over the same recorded instance corpus; and
6. emit a zero-finding parity receipt and a non-editable admissible Contract IR.

`program.json` is public-safe operational data governed by those authorities. It
contains logical organization names, public GitHub task links, and coarse evidence
states. It must not contain Cloudflare account IDs, bucket names, object keys,
access-key IDs, customer identifiers, state snapshots, provider payloads, secret
references, or credential values.

The runtime validator in `scripts/validate_r2_fleet_admission.mjs` enforces
cross-record invariants that shape schemas alone cannot express: exact task
inventory, dependency closure and acyclicity, unique organizations, bounded
evidence vocabulary, fail-closed admission, and absence of forbidden private
fields.
