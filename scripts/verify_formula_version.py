#!/usr/bin/env python3
"""Verify that a packaged BlueArch CLI reports one exact public version identity."""

from __future__ import annotations

import argparse
import re
import sys


PUBLIC_BINARIES = frozenset(
    {
        "bluearch-aws-core",
        "bluearch-aws-governance",
        "bluearch-aws-ops",
        "bluearch-aws-tags",
    }
)
BARE_SEMVER_RE = re.compile(r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$")


def verify_version_output(binary: str, expected: str, output: str) -> None:
    if binary not in PUBLIC_BINARIES:
        raise ValueError("binary is outside the public BlueArch package set")
    if not BARE_SEMVER_RE.fullmatch(expected):
        raise ValueError("expected version must be a bare semantic version")

    identity = re.compile(
        rf"^{re.escape(binary)} v?{re.escape(expected)}(?: \(production\))?$"
    )
    matches = [line.strip() for line in output.splitlines() if identity.fullmatch(line.strip())]
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one {binary} {expected} public version identity, "
            f"found {len(matches)} in {output!r}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", required=True)
    parser.add_argument("--expected", required=True)
    args = parser.parse_args()

    try:
        verify_version_output(args.binary, args.expected, sys.stdin.read())
    except ValueError as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
