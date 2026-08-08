# Go CLI portability CI standard

Every actively maintained Go command-line repository must compile, test, and execute its real CLI entry point on Linux, macOS, and Windows through GitHub Actions.

The reusable implementation is `.github/workflows/reusable-go-cli-portability.yml`. Production callers pin a full commit SHA only after the workflow has completed public test-organization certification.

## Required matrix

- `ubuntu-24.04`
- `macos-15`
- `windows-2025`

Explicit runner images avoid silent behavior changes from mutable `*-latest` aliases.

## Module and source contract

The caller supplies a repository-relative directory containing `go.mod` and, when needed, a repository-relative Go main package such as `.` or `./cmd/example`.

Each operating system runs:

1. Go installation from the caller's `go.mod`;
2. `go mod download` and `go mod verify` under `GOFLAGS=-mod=readonly`;
3. `gofmt` validation over every tracked Go source file;
4. `go vet ./...`;
5. `go test ./...`;
6. `go build -trimpath` for the selected main package into runner temporary storage;
7. the real built executable with `--help`;
8. a final clean-checkout assertion.

The selected package must report package name `main`. A library or repository placeholder must not receive a misleading green CLI workflow.

## Caller example

```yaml
name: Go CLI portability

on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  portability:
    uses: ORESoftware/.github/.github/workflows/reusable-go-cli-portability.yml@<full-commit-sha>
    with:
      working-directory: .
      main-package: .
      run-smoke: true
```

A repository whose executable lives below `cmd` selects it explicitly:

```yaml
    with:
      working-directory: .
      main-package: ./cmd/example
```

## Private module access

A caller with private Git module dependencies may pass a dedicated installation-scoped read credential:

```yaml
    secrets:
      cross-repo-token: ${{ secrets.CLI_CI_GITHUB_TOKEN }}
```

The credential must be restricted to the exact dependency repositories. Personal access tokens copied from chat, developer shells, or unrelated automation are not accepted CI credentials.

## Test-organization certification

Reusable workflow changes are first exercised from a public `*-test` organization using a dependency-free Go CLI fixture. Ubuntu, macOS, and Windows must all pass module verification, formatting, vet, tests, real executable build and smoke, and clean-worktree validation before the central workflow is merged.

Production rollout starts with public credential-free Go CLIs. Private modules, sibling working-tree dependencies, archived projects, duplicate aliases, and empty repositories are recorded separately and require an explicit preparation path rather than a weakened matrix.
