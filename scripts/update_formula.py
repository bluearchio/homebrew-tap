#!/usr/bin/env python3
"""Update a BlueArch Homebrew formula from a GitHub release asset."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FORMULA_URL_RE = re.compile(r'^\s*url ".*"$', re.MULTILINE)
FORMULA_VERSION_RE = re.compile(r'^\s*version ".*"$', re.MULTILINE)
FORMULA_SHA256_RE = re.compile(r'^\s*sha256 ".*"$', re.MULTILINE)
FORMULA_INSTALL_RE = re.compile(r'^\s*bin\.install .*$', re.MULTILINE)
DISABLE_RE = re.compile(r'^\s*disable! .*\n', re.MULTILINE)
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
SEMVER_TAG_RE = re.compile(
    r"^v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
PUBLIC_PACKAGES = frozenset(
    {
        "bluearch-aws-core",
        "bluearch-aws-governance",
        "bluearch-aws-ops",
        "bluearch-aws-tags",
    }
)


def replace_one(text: str, pattern: re.Pattern[str], replacement: str, label: str) -> str:
    count = len(pattern.findall(text))
    if count != 1:
        raise SystemExit(f"Expected exactly one {label} line, found {count}.")
    return pattern.sub(replacement, text, count=1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formula", required=True, type=Path)
    parser.add_argument("--repo", required=True, help="GitHub repo, for example bluearchio/bluearch-aws-core")
    parser.add_argument("--version", required=True, help="Release tag, for example v1.2.3")
    parser.add_argument("--asset", required=True, help="Release asset filename")
    parser.add_argument("--sha256", required=True, help="SHA256 of the release asset")
    parser.add_argument("--binary", required=True, help="Binary filename extracted by Homebrew")
    args = parser.parse_args()

    if args.binary not in PUBLIC_PACKAGES:
        allowed = ", ".join(sorted(PUBLIC_PACKAGES))
        raise SystemExit(f"--binary must be one of: {allowed}.")
    if args.formula.name != f"{args.binary}.rb":
        raise SystemExit("--formula filename must match --binary.")
    if args.repo != f"bluearchio/{args.binary}":
        raise SystemExit("--repo must match bluearchio/<binary>.")
    if args.asset != f"{args.binary}-macos-arm64.zip":
        raise SystemExit("--asset must match <binary>-macos-arm64.zip.")
    if not SEMVER_TAG_RE.fullmatch(args.version):
        raise SystemExit("--version must be a v-prefixed semantic version tag.")
    if not HEX64_RE.fullmatch(args.sha256):
        raise SystemExit("--sha256 must be 64 lowercase hex characters.")

    formula = args.formula
    text = formula.read_text(encoding="utf-8")
    url = f"https://github.com/{args.repo}/releases/download/{args.version}/{args.asset}"
    formula_version = args.version[1:]

    text = DISABLE_RE.sub("", text)
    text = replace_one(text, FORMULA_URL_RE, f'  url "{url}"', "url")
    text = replace_one(text, FORMULA_VERSION_RE, f'  version "{formula_version}"', "version")
    text = replace_one(text, FORMULA_SHA256_RE, f'  sha256 "{args.sha256}"', "sha256")
    text = replace_one(text, FORMULA_INSTALL_RE, f'    bin.install "{args.binary}"', "install")
    formula.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
