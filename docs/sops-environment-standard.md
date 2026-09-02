# ORESoftware SOPS environment-file standard

**Status:** v0.4 implementation merged and certified  
**Implementation:** `ORESoftware/ores-sops`  
**Implementation PR:** `ORESoftware/ores-sops#18`  
**Completed issue:** `ORESoftware/ores-sops#16`  
**Linear:** DEN-2636 parent, DEN-2637 implementation, DEN-2638 CI gates, DEN-2639 pilot, DEN-2641 key lifecycle  

## Decision

Repositories adopting the ORESoftware application-dotenv convention use exact,
per-environment SOPS ciphertext files:

```text
env/enc/dev.env.enc
env/enc/stage.env.enc   # optional exact third environment
env/enc/prod.env.enc
```

Development and production are required. Stage is optional, but when present it
must use exactly `stage`; aliases such as `staging`, `qa`, `release`, wildcard
rules, and arbitrary names are rejected.

Every plaintext dotenv file is local-only. Managed decrypted targets are:

```text
env/dec/dev.env
env/dec/stage.env
env/dec/prod.env
```

The active local environment is a relative managed symlink:

```text
.env -> env/dec/dev.env
# or
.env -> env/dec/stage.env
# or
.env -> env/dec/prod.env
```

The helper must never overwrite or remove an unmanaged root `.env` file or
symlink. Existing valid v0.3 repositories with only dev/prod remain valid until
they explicitly opt into stage.

## Access-control model

Access is granted per ciphertext file, not per repository.

A developer may clone the repository and see ciphertext filenames, encrypted
values, and public `age1...` recipient metadata. None of that grants decryption.
The developer's matching private age identity can decrypt only files whose exact
recipient list includes that public recipient.

A normal age recipient list is one-of-many. Therefore:

- an ordinary developer may be listed only on dev;
- a release engineer may be listed on dev and stage but omitted from prod;
- a production-authorized engineer may deliberately be listed on all three;
- dev, stage, and prod CI/deploy workloads should use separate identities;
- an independently controlled recovery identity may deliberately span all three.

Recommended matrix:

| Identity class | dev | stage | prod |
| --- | ---: | ---: | ---: |
| ordinary developer | yes | no | no |
| release engineer | yes | yes | no |
| production-authorized engineer | yes | yes | yes |
| dev CI workload | yes | no | no |
| stage deploy workload | no | yes | no |
| prod deploy workload | no | no | yes |
| offline recovery | yes | yes | yes |

A stage-enabled production policy must retain at least one true dev-only
recipient absent from both stage and prod. Repositories should also require at
least one stage recipient omitted from prod. A production-only hardware or
workload identity is recommended and can be enforced separately.

Private identities, application values, and decrypted dotenv files must never
appear in Git, Linear, issues, pull requests, chat, logs, screenshots, examples,
fixtures, caches, or artifacts.

## Canonical `.sops.yaml` pattern

Only public recipients belong in `.sops.yaml`:

```yaml
creation_rules:
  - path_regex: ^env/enc/dev\.env\.enc$
    age:
      - age1_DEV_DEVELOPER_REPLACE_WITH_REAL_PUBLIC_RECIPIENT
      - age1_DEV_CI_REPLACE_WITH_REAL_PUBLIC_RECIPIENT
      - age1_RECOVERY_REPLACE_WITH_REAL_PUBLIC_RECIPIENT

  - path_regex: ^env/enc/stage\.env\.enc$
    age:
      - age1_RELEASE_ENGINEER_REPLACE_WITH_REAL_PUBLIC_RECIPIENT
      - age1_STAGE_DEPLOY_REPLACE_WITH_REAL_PUBLIC_RECIPIENT
      - age1_RECOVERY_REPLACE_WITH_REAL_PUBLIC_RECIPIENT

  - path_regex: ^env/enc/prod\.env\.enc$
    age:
      - age1_PROD_OPERATOR_REPLACE_WITH_REAL_PUBLIC_RECIPIENT
      - age1_PROD_DEPLOY_REPLACE_WITH_REAL_PUBLIC_RECIPIENT
      - age1_RECOVERY_REPLACE_WITH_REAL_PUBLIC_RECIPIENT
```

A two-environment repository omits the exact stage rule and all stage material.
Any `.sops.yaml` rule targeting `env/enc/` must be one of the exact dev, optional
stage, or prod rules. Other SOPS artifact classes, such as narrowly scoped
KSOPS-encrypted Kubernetes Secret YAML, must use a separate path and policy.

## Desired policy versus current ciphertext access

Each ciphertext has its own random SOPS data-encryption key. SOPS wraps that file
key separately for the public recipients on the matching rule.

`.sops.yaml` is desired policy. Existing ciphertext retains its current wrapped
recipient metadata until that file is synchronized. Removing a public recipient
from `.sops.yaml` alone does not revoke the identity from current ciphertext.

After an access-policy change, update only the affected environment:

```sh
ores-sops sync-keys stage
```

Equivalent direct operation:

```sh
sops updatekeys -y --input-type dotenv env/enc/stage.env.enc
```

The access audit must compare desired recipients with actual public recipient
metadata and fail on drift.

## Initialization

Recommended scoped stage-enabled initialization:

```sh
ores-sops init \
  --with-stage \
  --stage-recipient age1_STAGE_PUBLIC_RECIPIENT \
  --prod-recipient age1_PROD_PUBLIC_RECIPIENT \
  --recovery-recipient age1_RECOVERY_PUBLIC_RECIPIENT
```

When scoped recipient options are used, the local identity begins as dev-only.
It is not added to stage or prod unless its public recipient is explicitly
provided there.

Supported options are repeatable:

```text
--recipient K           common/bootstrap recipient on every configured environment
--dev-recipient K       dev only
--stage-recipient K     stage only and enables stage
--prod-recipient K      prod only
--recovery-recipient K  every configured environment
```

Legacy `ores-sops init` remains a compatibility bootstrap. Its initial shared
recipient set must not be mistaken for a final least-privilege production
policy.

## Git ignore contract

A stage-enabled repository uses this deny/allow ordering:

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
!/env/enc/stage.env.enc
!/env/enc/prod.env.enc
```

A legacy dev/prod repository may omit the stage ciphertext exception while stage
is not configured. As soon as the exact stage rule exists, the stage exception
is required.

CI and local verification must prove ignore behavior with `git check-ignore
--no-index` and NUL-delimited tracked/staged path enumeration, not visual
inspection alone.

## SOPS format rules

The `.env.enc` suffix does not let SOPS infer the dotenv store. Every operation
must explicitly use:

```text
--input-type dotenv
--output-type dotenv
```

Encryption must also use the canonical destination as the filename override so
the exact creation rule is selected deterministically:

```text
--filename-override env/enc/stage.env.enc
```

## Filesystem and symlink boundary

Repository-controlled paths are untrusted until validated. The implementation
must fail closed rather than follow repository symlinks.

- `env`, `env/enc`, and `env/dec` must be real directories.
- Canonical ciphertext, plaintext, and helper state files must not be symlinks.
- `.sops.yaml`, `.gitignore`, `.gitattributes`, and `.env.example` must not be
  symlinks when read, written, or validated.
- Approved ciphertext and policy paths must not be tracked as Git mode `120000`.
- `env/dec` is mode `0700`; completed plaintext files are mode `0600` on POSIX.
- Temporary plaintext must be created beneath `env/dec` on the same filesystem
  as its final target so atomic rename is available.
- Catchable-signal and later `lock` cleanup must remove managed temp patterns.
- Stage ciphertext, stage plaintext, or a stage `.env` target without the exact
  stage rule must fail closed.

## Local activation rules

1. Accept only `dev`, configured `stage`, or `prod`.
2. Validate the managed tree before reading or writing.
3. Decrypt into an owner-only temporary file beneath `env/dec`.
4. Validate dotenv syntax and duplicate keys.
5. Leave the prior complete plaintext untouched on decrypt or validation
   failure.
6. Atomically install the completed file with mode `0600`.
7. Refuse an unmanaged root `.env`.
8. Atomically replace only the managed relative `.env` symlink.
9. Never infer production from a branch, missing lower environment, or Git ref.
10. `lock` removes managed dev, stage, and prod plaintext and stale managed temp
    state.

`ORESoftware/ores-sops` is the reference implementation.

## Required access gate

For stage-enabled repositories:

```sh
ores-sops verify

ores-sops-access-audit check \
  --require-stage \
  --require-stage-exclusive \
  --require-ciphertext
```

When a production-only identity is mandatory:

```sh
ores-sops-access-audit check \
  --require-stage \
  --require-stage-exclusive \
  --require-prod-exclusive \
  --require-ciphertext
```

Before ciphertext exists, only the explicit bootstrap mode may skip ciphertext
synchronization:

```sh
ores-sops-access-audit check \
  --require-stage \
  --require-stage-exclusive \
  --policy-only
```

Do not use `--policy-only` after ciphertext exists. The audit does not decrypt;
it reads exact public rules and public SOPS recipient metadata. Normal output
reports counts, not recipient strings.

## Authorization acceptance tests

Generated ephemeral identities must prove the negative matrix:

```text
dev identity:      dev succeeds; stage and prod fail
stage identity:    stage succeeds; dev and prod fail
prod identity:     prod succeeds; dev and stage fail
recovery identity: dev, stage, and prod succeed
```

An unauthorized activation must create neither the requested plaintext file nor
a managed `.env` link. A stage-only recipient change must not rewrite dev or
prod ciphertext.

## Git hook boundary

- Enumerate staged paths NUL-safely, including rename/copy/type-change cases.
- Reject plaintext at any depth, even when force-added.
- Reject every `env/enc/*` path except canonical configured paths.
- Reject stage ciphertext when the exact stage rule is absent.
- Refuse custom `core.hooksPath` by default; require explicit reviewed opt-in.
- Reject symlinked hook directories and hook files.
- Preserve unmanaged hooks rather than overwriting them.
- Shell-escape embedded helper paths.

## CI gates

Keyless pull-request CI must verify:

- root, nested, suffixed, and `env/dec/**` plaintext is ignored;
- exact dev/prod and configured stage ciphertext is trackable;
- no unexpected tracked `env/enc/*` or plaintext path exists;
- exact dev/prod and at most one exact stage rule exists;
- stage material cannot exist without the stage rule;
- desired and actual recipient sets agree for existing ciphertext;
- the stage-enabled matrix includes a true dev-only recipient;
- stage access remains narrower than prod when policy requires it;
- ciphertext looks like SOPS output and contains no obvious plaintext
  application assignment;
- tracked private age/PEM/OpenSSH key material is rejected without echoing it;
- `.gitattributes` normalizes `env/enc/*.env.enc` to LF;
- Docker/build/archive contexts cannot retain plaintext, ciphertext, or private
  identities;
- helper, access-audit, fleet-audit, and wrapper tests pass.

Fork-originated pull requests must never receive decryption identities.

Trusted protected jobs may additionally verify decryptability and application
startup without logging values. They must clean plaintext in an always-run
finalizer and never cache or upload it.

Security-sensitive workflows must pin third-party actions to immutable SHAs,
use least privilege, disable persisted checkout credentials when unnecessary,
bound runtime, and cancel superseded jobs where appropriate.

## Key lifecycle

- Give humans individual identities; never share one private human age key.
- Keep dev, stage, and prod workload identities separate.
- Prefer OIDC-backed KMS/workload identity for production automation.
- Keep at least one independently controlled recovery path.
- Run `sync-keys`/`updatekeys` after every recipient change.
- Rotate the SOPS data key after access removal when future ciphertext access
  must be strongly revoked.
- Rotate application credentials when an identity may have learned them.
- Remember that old Git commits may remain decryptable to historically
  authorized identities.
- Remove GitHub, cloud, VPN, shell, CI, and secret-manager permissions
  separately; SOPS controls ciphertext decryption only.

## Runtime ACLs and shared machines

SOPS controls whether an identity can decrypt. Once a file exists under
`env/dec`, it is ordinary plaintext protected by the local operating system.
Do not share one OS account between privileged and unprivileged developers.
Production plaintext should normally materialize only on protected deployment
workloads, not ordinary developer laptops. `sops-nix` owner/group/mode settings
may add a host runtime ACL, but do not replace recipient policy.

## Rollout sequence

1. Pin `ORESoftware/ores-sops` v0.4 or newer.
2. Preserve valid dev/prod repositories unchanged until stage is needed.
3. Opt into stage with the exact rule, Git allowlist, recipient matrix, helper,
   access audit, and tests together.
4. Use public dummy values for initial low-risk certification.
5. Exercise onboarding, offboarding, negative decrypts, recovery, and key
   synchronization.
6. Protect `.sops.yaml`, stage/prod ciphertext, helper/audit code, and deployment
   workflows with CODEOWNERS plus an enforced branch ruleset.
7. Roll out in small auditable batches and track exceptions rather than
   weakening the baseline.

## Acceptance criteria

- Dev and prod exact paths are required; stage is the only optional exact third
  application-dotenv environment.
- Dev-only access cannot decrypt stage or prod.
- Stage-limited access cannot decrypt prod when that boundary is required.
- Existing dev/prod repositories remain valid.
- Stage material without the exact stage rule fails closed.
- Plaintext is never tracked and managed local files remain owner-only.
- Desired and actual public recipient metadata cannot silently drift.
- Updating stage access does not alter dev or prod ciphertext.
- Managed paths cannot redirect reads/writes through symlinks.
- CI, logs, artifacts, caches, Docker contexts, and release archives retain no
  decrypted dotenv material or private identity.
