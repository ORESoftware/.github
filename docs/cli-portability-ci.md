# CLI portability CI standard

Every actively maintained command-line repository must compile, test, and execute its CLI entry points on Linux, macOS, and Windows through GitHub Actions.

The reusable implementation is `.github/workflows/reusable-cli-portability.yml`. Callers pin an immutable commit after the workflow has completed its test-organization certification.

## Required matrix

- `ubuntu-24.04`
- `macos-15`
- `windows-2025`

The matrix is intentionally explicit rather than using mutable `*-latest` runner labels. A runner-image update must be reviewed and certified as a source change.

## Rust contract

A Rust caller must provide a `Cargo.toml` containing at least one binary target. By default, a committed `Cargo.lock` is required and every Cargo command uses `--locked`.

Each operating system runs:

1. `cargo fmt --all -- --check`;
2. warnings-denied Clippy for all targets;
3. all locked tests with output retained;
4. a locked release build of every binary;
5. every release binary with `--help`;
6. a final clean-checkout assertion.

Repositories that deliberately do not commit a lockfile must set `cargo-locked: false` explicitly. This is an exception, not the fleet default.

## Node contract

A Node caller selects `npm`, `pnpm`, or Yarn and uses the corresponding immutable/frozen install mode. The workflow executes each available script in this order:

1. `format:check`;
2. `lint`;
3. `typecheck`;
4. `test`;
5. `build`.

At least `test` or `build` is required. Every `package.json#bin` entry is then executed with `--help`, followed by a clean-checkout assertion.

## Caller example

```yaml
name: CLI portability

on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  portability:
    uses: ORESoftware/.github/.github/workflows/reusable-cli-portability.yml@<full-commit-sha>
    with:
      language: rust
      rust-toolchain: stable
      cargo-locked: true
      run-smoke: true
```

A private CLI with private cross-repository Git dependencies may pass a dedicated read-only repository secret:

```yaml
    secrets:
      cross-repo-token: ${{ secrets.CLI_CI_GITHUB_TOKEN }}
```

The secret must be a short-lived or installation-scoped read credential restricted to the exact dependency repositories. Personal access tokens copied from chat, developer shells, or unrelated automation are not an accepted CI credential.

## Path dependencies

A CLI that depends on sibling working trees must prepare those exact immutable siblings in a repository-specific wrapper before calling or reproducing the matrix. It must not silently replace path dependencies with mutable branch downloads.

## Test-organization certification

Changes to the reusable workflow are first exercised from a public `*-test` organization with minimal Rust and Node CLI fixtures. All six operating-system/language jobs must pass before the reusable workflow is merged and pinned by production callers.

Production rollout begins with `zed-pkg/zed-cli`, followed by buildable `*-cli` repositories. Empty placeholders, archived repositories, duplicate aliases, and repositories without an executable entry point are recorded separately rather than receiving a misleading green workflow.
