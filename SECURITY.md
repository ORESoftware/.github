# Security policy

Report suspected vulnerabilities privately through GitHub's security-advisory flow when available. Do not open a public issue containing exploit details, credentials, private data, or unredacted logs.

Security fixes should include a clear threat model, affected boundary, regression test, rollout plan, and rollback path. Rotate any credential that may have been exposed; deleting it from a later commit is not sufficient.

## Repository environment secrets

Repositories that adopt SOPS-managed application dotenv secrets must follow the
organization standard in
[`docs/sops-environment-standard.md`](docs/sops-environment-standard.md).

The approved tracked paths are exactly:

```text
env/enc/dev.env.enc
env/enc/stage.env.enc   # optional exact third environment
env/enc/prod.env.enc
```

Dev and prod are required. Stage is optional. `staging`, `qa`, wildcard rules,
arbitrary names, and all other `env/enc/*` paths are rejected.

Plaintext stays only under ignored `env/dec/{dev,stage,prod}.env`. The managed
root `.env` is a relative symlink to one configured ignored target, never a
copied plaintext file. CI and local hooks must reject force-added plaintext,
unexpected ciphertext paths, symlink redirection, and stage material without the
exact stage rule.

Repository read access is not decryption authorization. Every ciphertext has an
independent recipient list. An ordinary developer may receive dev-only access
and must fail to decrypt stage or prod. Stage-limited identities must be omitted
from prod where that boundary is required. Protected production workloads and
an independently controlled recovery identity should use separate credentials.

Changing `.sops.yaml` does not by itself change existing ciphertext access. Run
`ores-sops sync-keys <environment>` or `sops updatekeys` for each affected file,
then require the desired-versus-actual recipient metadata audit. Do not use
`--policy-only` to bypass checks after ciphertext exists.

Private SOPS/age identities and decrypted values must never be placed in Git,
issues, pull requests, Linear, chat, logs, examples, screenshots, caches, or
build artifacts. Do not expose any decryption identity to fork-originated pull
requests.

Once decrypted material exists, it is ordinary plaintext subject to local OS
permissions. Do not share one OS account between privileged and unprivileged
developers. Production plaintext should normally materialize only on protected
deployment workloads, not ordinary developer laptops.

<!-- ore-org-baseline:begin -->
## Reporting a vulnerability

Do **not** open a public issue for a suspected vulnerability, exposed credential, authentication bypass, data leak, or sensitive infrastructure weakness.

Use private vulnerability reporting from the **Security** tab of the affected repository when available. Otherwise contact the organization owners through an established private operational channel and identify the affected repository, impact, reproduction conditions, and a safe contact method. Provide only the minimum evidence needed; do not include live credentials, private keys, customer data, or destructive proof-of-concept payloads.

## Handling exposed credentials

Treat any credential pasted into chat, logs, commits, issues, pull requests, build artifacts, screenshots, or test fixtures as compromised. Stop using it, revoke or rotate it, replace dependent configuration, and audit recent use. Removing a secret from the latest file does not invalidate it or erase earlier copies. Repository-history rewriting requires exact authorization and coordinated review.

## Supported versions and response expectations

Each repository documents its own supported versions. No service-level response commitment is implied by this fallback policy. Maintainers should acknowledge valid reports privately, limit access, preserve evidence, coordinate remediation, test the fix, rotate affected secrets, and disclose responsibly when appropriate.

Linear planning context: [github.com/ORESoftware](https://linear.app/denman/project/githubcomoresoftware-1574ce77fadf).
<!-- ore-org-baseline:end -->
