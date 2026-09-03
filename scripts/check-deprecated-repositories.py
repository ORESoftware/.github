#!/usr/bin/env python3
"""Validate the public, machine-readable ORESoftware deprecation registry."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "deprecated-repositories.json"
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
URL_RE = re.compile(r"^https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)$")
ALLOWED_CHANGE_CLASSES = {
    "deprecation",
    "security-remediation",
    "migration",
    "compatibility",
    "historical-reference",
}
REQUIRED_ROUTES = {
    "ORESoftware/ai-agent-bridge.rs": "agent-pontifex/ai-agent-bridge.rs",
    "ORESoftware/shared-auth-server.rs": "shared-auth/shared-auth-server.rs",
}
ROUTING_SURFACES = {
    ROOT / "AGENTS.md": "<!-- ores-deprecation-routing: 2026-09-03 -->",
    ROOT / "profile/README.md": "<!-- ores-deprecated-repositories: 2026-09-03 -->",
}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def main() -> int:
    failures: list[str] = []
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schemaVersion") != "ores.deprecated-repositories.v1":
        fail("unsupported schemaVersion", failures)
    owner = data.get("owner")
    if owner != "ORESoftware":
        fail("owner must be ORESoftware", failures)

    rows = data.get("repositories")
    if not isinstance(rows, list) or not rows:
        fail("repositories must be a non-empty array", failures)
        rows = []

    seen: set[str] = set()
    observed_routes: dict[str, str] = {}
    for index, row in enumerate(rows):
        prefix = f"repositories[{index}]"
        if not isinstance(row, dict):
            fail(f"{prefix} must be an object", failures)
            continue
        expected = {
            "repository", "status", "canonicalRepository", "canonicalUrl",
            "releasesAllowed", "allowedChangeClasses",
        }
        if set(row) != expected:
            fail(f"{prefix} fields must be exactly {sorted(expected)}", failures)
        repository = row.get("repository")
        canonical = row.get("canonicalRepository")
        if not isinstance(repository, str) or not REPOSITORY_RE.fullmatch(repository):
            fail(f"{prefix}.repository is invalid", failures)
        elif not repository.startswith(f"{owner}/"):
            fail(f"{prefix}.repository must belong to {owner}", failures)
        elif repository in seen:
            fail(f"duplicate repository {repository}", failures)
        else:
            seen.add(repository)
        if not isinstance(canonical, str) or not REPOSITORY_RE.fullmatch(canonical):
            fail(f"{prefix}.canonicalRepository is invalid", failures)
        elif canonical == repository:
            fail(f"{prefix} canonical repository must differ", failures)
        elif isinstance(repository, str):
            observed_routes[repository] = canonical
        match = URL_RE.fullmatch(str(row.get("canonicalUrl", "")))
        if not match or match.group(1) != canonical:
            fail(f"{prefix}.canonicalUrl must exactly match canonicalRepository", failures)
        if row.get("status") != "deprecated":
            fail(f"{prefix}.status must be deprecated", failures)
        if row.get("releasesAllowed") is not False:
            fail(f"{prefix}.releasesAllowed must be false", failures)
        classes = row.get("allowedChangeClasses")
        if (
            not isinstance(classes, list)
            or set(classes) != ALLOWED_CHANGE_CLASSES
            or len(classes) != len(ALLOWED_CHANGE_CLASSES)
        ):
            fail(
                f"{prefix}.allowedChangeClasses must contain the complete frozen set",
                failures,
            )

    if observed_routes != REQUIRED_ROUTES:
        fail("registry must contain exactly the reviewed canonical routes", failures)

    documentation = (ROOT / "docs/deprecated-repositories.md").read_text(
        encoding="utf-8"
    )
    for repository, canonical in sorted(REQUIRED_ROUTES.items()):
        if repository not in documentation:
            fail(f"documentation omits {repository}", failures)
        if canonical not in documentation:
            fail(f"documentation omits {canonical}", failures)

    for path, marker in ROUTING_SURFACES.items():
        text = path.read_text(encoding="utf-8")
        if not text.startswith(marker):
            fail(f"{path.relative_to(ROOT)} must begin with {marker}", failures)
        header = text[:2500]
        for repository, canonical in sorted(REQUIRED_ROUTES.items()):
            if repository not in header:
                fail(f"{path.relative_to(ROOT)} omits {repository} near the top", failures)
            if canonical not in header:
                fail(f"{path.relative_to(ROOT)} omits {canonical} near the top", failures)

    migration = (
        ROOT / "docs/migrations/ai-agent-bridge-to-agent-pontifex.md"
    ).read_text(encoding="utf-8")
    for value in (
        "ORESoftware/ai-agent-bridge.rs",
        "agent-pontifex/ai-agent-bridge.rs",
        "Consumer migration gate",
    ):
        if value not in migration:
            fail(f"AI-agent bridge migration evidence omits {value}", failures)

    if failures:
        for message in failures:
            print(f"ERROR: {message}", file=sys.stderr)
        return 1
    print(f"deprecated repository registry: PASS ({len(rows)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
