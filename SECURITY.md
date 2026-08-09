# Security policy

Report suspected vulnerabilities privately through GitHub's security-advisory flow when available. Do not open a public issue containing exploit details, credentials, private data, or unredacted logs.

Security fixes should include a clear threat model, affected boundary, regression test, rollout plan, and rollback path. Rotate any credential that may have been exposed; deleting it from a later commit is not sufficient.

## Repository environment secrets

Repositories that adopt SOPS-managed dotenv secrets must follow the organization standard in [`docs/sops-environment-standard.md`](docs/sops-environment-standard.md).

The approved tracked secret-bearing paths are exactly:

```text
env/enc/dev.env.enc
env/enc/prod.env.enc
```

Plaintext dotenv files remain ignored at every depth. The managed root `.env` is a relative symlink to an ignored `env/dec/dev.env` or `env/dec/prod.env`, never a copied plaintext file. CI and local hooks must reject force-added plaintext and unexpected files below `env/enc/`.

Private SOPS/age identities and decrypted values must never be placed in Git, issues, pull requests, Linear, chat, logs, examples, screenshots, caches, or build artifacts.

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
