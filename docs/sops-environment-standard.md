# ORESoftware SOPS environment-file standard

**Status:** rollout standard / pilot implementation in review  
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

Use the explicit deny/allow rules below. The nested patterns intentionally encode the organization requirement even where Git pattern semantics overlap.

```gitignore
*.env
*/*.env
*/**/*.env
.env.*
!.env.example

/env/dec/

/env/enc/*
!/env/enc/dev.env.enc
!/env/enc/prod.env.enc
```

CI and local verification must prove this with `git check-ignore --no-index` and `git ls-files`, not merely by visually inspecting `.gitignore`.

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

## Local activation rules

1. Resolve only `dev` or `prod`; arbitrary environment names are rejected.
2. Decrypt into an owner-only temporary file under `env/dec/`.
3. Do not replace an existing complete plaintext file unless decryption succeeds.
4. Set the completed plaintext file to mode `0600` where the platform supports POSIX modes.
5. Atomically rename the completed plaintext file into `env/dec/<env>.env`.
6. Refuse to overwrite an unmanaged root `.env` file or symlink.
7. Atomically replace the managed root symlink with a relative link to the selected target.
8. Never infer production from branch names, missing development state, or current Git ref.

`ORESoftware/ores-sops` is the reference helper for this contract.

## Editing

Prefer editing ciphertext through SOPS rather than routinely editing durable plaintext. When a plaintext edit workflow is used, the helper must detect local edits and refuse to silently clobber them.

Status commands, CI output, logs, and automation evidence must never print decrypted values.

## CI gates

### Keyless pull-request checks

Every adopting repository should be able to run these without a decryption identity:

- root `.env`, nested `*.env`, and `env/dec/**` are ignored;
- `env/enc/dev.env.enc` and `env/enc/prod.env.enc` are not ignored;
- no tracked path ends in plaintext `.env` material;
- no unexpected tracked file exists under `env/enc/`;
- `.sops.yaml` contains exact dev/prod path rules;
- ciphertext files contain SOPS metadata rather than obvious plaintext;
- force-added plaintext and private identity material are rejected;
- helper tests cover unmanaged `.env` refusal, path allowlisting, atomic failure, and symlink safety;
- build/archive/container contexts cannot accidentally retain decrypted files.

Fork-originated pull requests must not receive a decryption identity.

### Trusted checks

Protected branch/environment or manually approved trusted workflows may additionally:

- verify SOPS MAC/decryptability;
- validate dotenv syntax and repository-specific required-key schema;
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

1. Land the exact contract and tests in `ORESoftware/ores-sops`.
2. Add organization security/agent guidance in `ORESoftware/.github`.
3. Pilot with dummy values in one low-risk repository that already expects root `.env`.
4. Certify Linux and macOS; explicitly certify Windows symlink behavior or document a repository/platform exception.
5. Add protected development identities and exercise recipient add/remove workflows.
6. Establish distinct production recipient/KMS policy and recovery drill.
7. Roll out in small batches, prioritizing repositories already using reproducible Nix environments and flags-2-env conventions.
8. Track every exception rather than weakening the baseline silently.

## Acceptance criteria

- Exactly `env/enc/dev.env.enc` and `env/enc/prod.env.enc` are approved tracked secret-bearing paths.
- No plaintext `.env` file is tracked at any depth.
- Root `.env` is absent or a managed relative symlink to `env/dec/dev.env` or `env/dec/prod.env`.
- Decrypt failure never replaces a prior complete plaintext file with partial/empty output.
- Unmanaged root `.env` state is never overwritten or deleted.
- SOPS dotenv format selection is explicit.
- Dev-only access cannot decrypt the final production policy.
- Fork pull requests never receive decryption identities.
- CI, logs, artifacts, caches, Docker contexts, and release archives retain no decrypted dotenv material.
