#!/usr/bin/env python3
"""Update a BlueArch Homebrew formula from a GitHub release asset."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


URL_RE = re.compile(r'^\s*url ".*"$', re.MULTILINE)
VERSION_RE = re.compile(r'^\s*version ".*"$', re.MULTILINE)
SHA256_RE = re.compile(r'^\s*sha256 ".*"$', re.MULTILINE)
INSTALL_RE = re.compile(r'^\s*bin\.install .*$',
                        re.MULTILINE)
DISABLE_RE = re.compile(r'^\s*disable! .*\n', re.MULTILINE)
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
SAFE_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def replace_one(text: str, pattern: re.Pattern[str], replacement: str, label: str) -> str:
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"Expected exactly one {label} line, found {count}.")
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formula", required=True, type=Path)
    parser.add_argument("--repo", required=True, help="GitHub repo, for example bluearchio/bluearch-aws-core")
    parser.add_argument("--version", required=True, help="Release tag, for example v1.2.3")
    parser.add_argument("--asset", required=True, help="Release asset filename")
    parser.add_argument("--sha256", required=True, help="SHA256 of the release asset")
    parser.add_argument("--binary", required=True, help="Binary filename extracted by Homebrew")
    args = parser.parse_args()

    if "/" not in args.repo or args.repo.startswith("/") or args.repo.endswith("/"):
        raise SystemExit("--repo must be in owner/name form.")
    if not args.version.startswith("v"):
        raise SystemExit("--version must be a tag that starts with v.")
    if not HEX64_RE.fullmatch(args.sha256):
        raise SystemExit("--sha256 must be 64 lowercase hex characters.")
    for label, value in (("--asset", args.asset), ("--binary", args.binary)):
        if not SAFE_NAME_RE.fullmatch(value):
            raise SystemExit(f"{label} contains unsupported characters.")

    formula = args.formula
    text = formula.read_text(encoding="utf-8")
    url = f"https://github.com/{args.repo}/releases/download/{args.version}/{args.asset}"

    text = DISABLE_RE.sub("", text)
    text = replace_one(text, URL_RE, f'  url "{url}"', "url")
    text = replace_one(text, VERSION_RE, f'  version "{args.version}"', "version")
    text = replace_one(text, SHA256_RE, f'  sha256 "{args.sha256}"', "sha256")
    text = replace_one(text, INSTALL_RE, f'    bin.install "{args.binary}"', "install")
    formula.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
