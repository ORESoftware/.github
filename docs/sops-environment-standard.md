# ORESoftware SOPS environment-file standard

**Status:** rollout standard / implementation merged / security-hardening audit in review  
**Linear:** DEN-2636 parent, DEN-2637 implementation, DEN-2638 CI gates, DEN-2639 pilot, DEN-2641 key lifecycle  
**Implementation:** `ORESoftware/ores-sops`  
**Portfolio project:** https://github.com/orgs/ORESoftware/projects/1

## Decision

Repositories adopting the ORESoftware SOPS dotenv convention track exactly these secret-bearing files:

```text
env/enc/dev.env.enc
env/enc/prod.env.enc
```

Every plaintext dotenv file is local-only. The managed decrypted targets are:

```text
env/dec/dev.env
env/dec/prod.env
```

The active local environment is exposed through a relative root symlink:

```text
.env -> env/dec/dev.env
# or
.env -> env/dec/prod.env
```

The helper must refuse to overwrite or remove a root `.env` that it does not own.

## Git ignore contract

Use the explicit deny/allow rules below. The nested patterns intentionally encode the organization requirement even where Git pattern semantics overlap. The `*.env.*` rule also covers common plaintext variants such as `service.env.local` and `service.env.production`; the exact ciphertext paths are re-allowed afterward.

```gitignore
*.env
*/*.env
*/**/*.env
.env.*
*.env.*
!.env.example

/env/dec/

/env/enc/*
!/env/enc/dev.env.enc
!/env/enc/prod.env.enc
```

CI and local verification must prove this with `git check-ignore --no-index` and NUL-delimited `git ls-files -z` / staged-path enumeration, not merely by visually inspecting `.gitignore`.

No other path below `env/enc/` is an approved tracked secret-bearing path.

## SOPS format rules

The `.env.enc` suffix means SOPS cannot infer the dotenv store from the final filename extension. Every SOPS operation must explicitly select dotenv input and output types.

Encryption must also use the destination path as the SOPS filename override so exact creation rules are chosen deterministically:

```text
--input-type dotenv
--output-type dotenv
--filename-override env/enc/dev.env.enc
```

Use separate exact creation rules for dev and prod. A bootstrap pilot may initially use one local public recipient, but production adoption must replace the production recipient set with a distinct protected identity or KMS policy.

Any `.sops.yaml` rule that targets `env/enc/` must be one of the two exact dev/prod rules. Wildcard, staging, release, QA, catch-all, or other noncanonical `env/enc` rules are rejected. Other SOPS artifact classes, such as narrowly scoped KSOPS-encrypted Kubernetes Secret YAML, must use a separate path/policy and do not broaden this dotenv namespace.

## Filesystem and symlink boundary

Repository-controlled paths are untrusted until validated. An adopting implementation must fail closed rather than follow repository symlinks for managed secret or policy paths.

- `env`, `env/enc`, and `env/dec` must be real directories, not symlinks.
- `env/enc/dev.env.enc`, `env/enc/prod.env.enc`, managed decrypted files, and helper state files must not be symlinks when read or written.
- `.sops.yaml`, `.gitignore`, `.gitattributes`, and `.env.example` must not be symlinks when the helper may write or validate them.
- Approved ciphertext and policy paths must not be tracked as Git symlinks (`120000` mode).
- `env/dec` should be mode `0700` on POSIX systems; decrypted dotenv files are `0600`.
- Decrypted temporary files must live on the same filesystem as their final destination so atomic rename is available.
- Temporary plaintext and diff baselines must be cleaned on normal exit and catchable termination signals. `SIGKILL` cannot be trapped, so `clean`/`lock` must also remove stale managed temp patterns from prior interrupted runs.

The purpose of these rules is to prevent a malicious or accidentally malformed checkout from redirecting decrypt, encrypt, edit, lock, or scaffold operations to paths outside the repository.

## Local activation rules

1. Resolve only `dev` or `prod`; arbitrary environment names are rejected.
2. Validate the managed directory tree and reject symlink escapes before reading or writing.
3. Decrypt into an owner-only temporary file under `env/dec/`.
4. Validate dotenv syntax and reject duplicate variable names before installation.
5. Do not replace an existing complete plaintext file unless decryption and validation both succeed.
6. Set the completed plaintext file to mode `0600` where the platform supports POSIX modes.
7. Atomically rename the completed plaintext file into `env/dec/<env>.env`.
8. Refuse to overwrite an unmanaged root `.env` file or symlink.
9. Atomically replace the managed root symlink with a relative link to the selected target.
10. Never infer production from branch names, missing development state, or current Git ref.

`ORESoftware/ores-sops` is the reference helper for this contract.

## Editing and non-secret output

Prefer editing ciphertext through SOPS rather than routinely editing durable plaintext. When a plaintext edit workflow is used, the helper must detect local edits and refuse to silently clobber them.

Diff/status commands, CI output, logs, and automation evidence must never print decrypted values. A safe diff may report key names and whether a key was added, removed, or changed by hashing values internally without printing those values.

Keyless ciphertext validation must reject an approved `.env.enc` file when a normal application assignment is visibly plaintext even if SOPS metadata is also present. Private-key scans must fail without echoing the matching secret line.

## Git hook boundary

Git configuration is repository-controlled state and may redirect hook writes outside `.git`.

- Use NUL-delimited staged-path enumeration so newline-containing filenames cannot bypass checks.
- Include rename, copy, modification, type-change, and other non-deletion changes; a rename into `*.env` must be blocked.
- Refuse a custom `core.hooksPath` by default. If a repository intentionally uses one, require an explicit reviewed opt-in rather than silently writing through it.
- Reject symlinked hook directories and hook files before writing.
- Preserve unmanaged hooks rather than overwriting them.
- Shell-escape any absolute helper path embedded into generated hooks.

## CI gates

### Keyless pull-request checks

Every adopting repository should be able to run these without a decryption identity:

- root `.env`, nested `*.env`, common `*.env.*` variants, and `env/dec/**` are ignored;
- `env/enc/dev.env.enc` and `env/enc/prod.env.enc` are not ignored;
- no tracked plaintext dotenv path exists, including rename/newline-filename edge cases;
- no unexpected tracked file exists under `env/enc/`;
- approved ciphertext and policy files are not tracked symlinks;
- `.sops.yaml` contains exact dev/prod path rules and no broad/noncanonical `env/enc` rule;
- ciphertext files contain SOPS metadata and no obvious plaintext application assignment;
- tracked private age/PEM/OpenSSH identity material is rejected without printing the match;
- `.gitattributes` normalizes `env/enc/*.env.enc` to LF;
- helper tests cover unmanaged `.env` refusal, path allowlisting, atomic failure, symlink escapes, custom hook paths, hook symlinks, duplicate dotenv keys, temp cleanup, and NUL-safe Git filenames;
- build/archive/container contexts cannot accidentally retain decrypted files.

Fork-originated pull requests must not receive a decryption identity.

### CI supply-chain requirements

Security-sensitive workflows should minimize the CI execution surface:

- pin third-party GitHub Actions to immutable full commit SHAs; comments may record the reviewed release tag;
- use `contents: read` or narrower permissions where possible;
- disable persisted checkout credentials when no push is required;
- bound job runtime with timeouts;
- use concurrency cancellation for superseded PR runs where appropriate;
- do not pass production SOPS identities to ordinary pull-request workflows.

### Trusted checks

Protected branch/environment or manually approved trusted workflows may additionally:

- verify SOPS MAC/decryptability;
- validate dotenv syntax, duplicate keys, and repository-specific required-key schema;
- smoke-test application startup without logging secrets;
- clean temporary plaintext in an always-run finalizer.

Never cache, upload, artifact, or summarize decrypted dotenv files.

## Key lifecycle

- Give humans individual identities; do not share one private human age identity.
- Keep development and production recipient policies separate.
- Prefer OIDC-backed KMS/workload identity for production CI when practical.
- Keep at least one independently controlled recovery path.
- Run `sops updatekeys` after recipient changes.
- Rotate the SOPS data key after removing access where future ciphertext access must be revoked.
- Rotate application credentials whenever compromise, offboarding, or historical access requires it.
- Remember that old Git commits remain decryptable to identities that had access to those historical ciphertext revisions.

Private identities and real secret values must never be stored in Git, Linear, GitHub issues or pull-request text, chat, logs, test fixtures, screenshots, build artifacts, or caches.

## Rollout sequence

1. Land and maintain the exact contract and adversarial tests in `ORESoftware/ores-sops`.
2. Keep organization security/agent guidance in `ORESoftware/.github` synchronized with the implementation.
3. Pilot with dummy values in one low-risk repository that already expects root `.env`.
4. Certify Linux and macOS; explicitly certify Windows symlink behavior or document a repository/platform exception.
5. Add protected development identities and exercise recipient add/remove workflows.
6. Establish distinct production recipient/KMS policy and recovery drill.
7. Roll out in small batches, prioritizing repositories already using reproducible Nix environments and flags-2-env conventions.
8. Track every exception rather than weakening the baseline silently.

## Acceptance criteria

- Exactly `env/enc/dev.env.enc` and `env/enc/prod.env.enc` are approved tracked application-dotenv secret-bearing paths.
- No plaintext `.env` or common `.env.*` variant is tracked at any depth except the explicitly safe `.env.example` schema file.
- Managed env/policy paths cannot redirect helper reads/writes through symlinks.
- Root `.env` is absent or a managed relative symlink to `env/dec/dev.env` or `env/dec/prod.env`.
- Decrypt failure or malformed/duplicate dotenv content never replaces a prior complete plaintext file.
- Unmanaged root `.env` state is never overwritten or deleted.
- SOPS dotenv format selection is explicit and `env/enc` creation rules are exact.
- Git checks are NUL-safe and include rename/type-change cases.
- Custom/external hooks paths and symlinked hooks cannot receive helper writes without explicit reviewed opt-in.
- Dev-only access cannot decrypt the final production policy.
- Fork pull requests never receive decryption identities.
- CI actions are immutably pinned and use least privilege.
- CI, logs, artifacts, caches, Docker contexts, and release archives retain no decrypted dotenv material.
