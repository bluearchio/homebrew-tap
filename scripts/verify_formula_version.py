#!/usr/bin/env python3
"""Verify that a packaged BlueArch CLI reports one exact public version identity."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PUBLIC_BINARIES = frozenset(
    {
        "bluearch-aws-core",
        "bluearch-aws-governance",
        "bluearch-aws-ops",
        "bluearch-aws-tags",
    }
)
BARE_SEMVER_RE = re.compile(r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
LEGACY_DIST_RELEASES = {
    "bluearch-aws-core": (
        "0.2.5",
        "https://dist.bluearch.io/releases/bluearch-aws-core/v0.2.5/bluearch-aws-core-macos-arm64.zip",
        "783493fdcd18ac0a27c06a37b96ab90cd2c35e64a027f02d26d05910b86121fd",
    ),
    "bluearch-aws-governance": (
        "0.2.3",
        "https://dist.bluearch.io/releases/bluearch-aws-governance/v0.2.3/bluearch-aws-governance-macos-arm64.zip",
        "9b1356098157682c724f1f18bda414337fad688a6d0ab0c4574ac0fecb16b653",
    ),
    "bluearch-aws-ops": (
        "0.13.3",
        "https://dist.bluearch.io/releases/bluearch-aws-ops/v0.13.3/bluearch-aws-ops-macos-arm64.zip",
        "7a3b875b53215ba382021c28bdd105433423048444489b76a516315350c7335e",
    ),
    "bluearch-aws-tags": (
        "0.12.3",
        "https://dist.bluearch.io/releases/bluearch-aws-tags/v0.12.3/bluearch-aws-tags-macos-arm64.zip",
        "fc8644656df517ff87b236bf6f1919de48dfa1c7482aeda9022692643b278b10",
    ),
}
LEGACY_VERSION_OUTPUTS = {
    "bluearch-aws-core": ("bluearch-core 0.2.5",),
    "bluearch-aws-governance": ("0.2.3",),
    "bluearch-aws-ops": (
        "BlueArch CLI version: v0.13.3",
        "Check for updates with brew update && brew outdated",
        "bluearchio/tap/bluearch-aws-ops.",
    ),
    "bluearch-aws-tags": (
        "No .env file found. Using system environment variables only.",
        "OK Local cache initialized",
        "AWS Tag Manager CLI v0.12.3 (production)",
        "You are up to date!",
    ),
}


def load_legacy_exceptions(path: Path) -> frozenset[str]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read legacy exception config: {error}") from error

    if not isinstance(document, dict) or set(document) != {"enabled"}:
        raise ValueError("legacy exception config must contain only an enabled list")
    enabled = document["enabled"]
    if not isinstance(enabled, list) or any(not isinstance(name, str) for name in enabled):
        raise ValueError("legacy exception config enabled value must be a list of names")
    if len(enabled) != len(set(enabled)):
        raise ValueError("legacy exception config contains duplicate names")
    unknown = set(enabled) - PUBLIC_BINARIES
    if unknown:
        raise ValueError(f"legacy exception config contains unknown names: {sorted(unknown)}")
    return frozenset(enabled)


def verify_version_output(
    binary: str,
    expected: str,
    source_url: str,
    sha256: str,
    output: str,
    legacy_exceptions: Path,
) -> None:
    if binary not in PUBLIC_BINARIES:
        raise ValueError("binary is outside the public BlueArch package set")
    if not BARE_SEMVER_RE.fullmatch(expected):
        raise ValueError("expected version must be a bare semantic version")
    if not HEX64_RE.fullmatch(sha256):
        raise ValueError("formula checksum must be 64 lowercase hexadecimal characters")

    enabled_legacy_exceptions = load_legacy_exceptions(legacy_exceptions)
    if (
        binary in enabled_legacy_exceptions
        and (expected, source_url, sha256) == LEGACY_DIST_RELEASES[binary]
    ):
        legacy_lines = tuple(line.rstrip(" ") for line in output.splitlines())
        if legacy_lines != LEGACY_VERSION_OUTPUTS[binary]:
            raise ValueError(
                f"expected the exact pinned legacy {binary} version identity, "
                f"got {output!r}"
            )
        return

    expected_url = (
        f"https://github.com/bluearchio/{binary}/releases/download/"
        f"v{expected}/{binary}-macos-arm64.zip"
    )
    if source_url != expected_url:
        raise ValueError(
            "only the exact pinned legacy dist release or the matching immutable "
            "GitHub Release URL is allowed"
        )

    identity = re.compile(
        rf"^{re.escape(binary)} v?{re.escape(expected)}(?: \(production\))?$"
    )
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    if len(lines) != 1 or not identity.fullmatch(lines[0]):
        raise ValueError(
            f"expected only one exact {binary} {expected} public version identity, "
            f"got {output!r}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", required=True)
    parser.add_argument("--expected", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--legacy-exceptions", required=True, type=Path)
    args = parser.parse_args()

    try:
        verify_version_output(
            args.binary,
            args.expected,
            args.source_url,
            args.sha256,
            sys.stdin.read(),
            args.legacy_exceptions,
        )
    except ValueError as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
