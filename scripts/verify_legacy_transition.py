#!/usr/bin/env python3
"""Enforce the one-way transition away from pinned legacy formula assets."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Optional

if __package__:
    from .verify_formula_version import LEGACY_DIST_RELEASES, load_legacy_exceptions
else:
    from verify_formula_version import LEGACY_DIST_RELEASES, load_legacy_exceptions


FORMULA_FIELDS = (
    ("version", re.compile(r'^\s+version "([^"]+)"$', re.MULTILINE)),
    ("url", re.compile(r'^\s+url "([^"]+)"$', re.MULTILINE)),
    ("sha256", re.compile(r'^\s+sha256 "([^"]+)"$', re.MULTILINE)),
)


def formula_release_tuple(formula: Path) -> tuple[str, str, str]:
    try:
        text = formula.read_text(encoding="utf-8")
    except OSError as error:
        raise ValueError(f"cannot read formula {formula}: {error}") from error

    values: list[str] = []
    for label, pattern in FORMULA_FIELDS:
        matches = pattern.findall(text)
        if len(matches) != 1:
            raise ValueError(
                f"expected exactly one {label} in {formula}, found {len(matches)}"
            )
        values.append(matches[0])
    return values[0], values[1], values[2]


def verify_current_state(current_config: Path, formula_dir: Path) -> frozenset[str]:
    current = load_legacy_exceptions(current_config)
    for binary, approved_tuple in LEGACY_DIST_RELEASES.items():
        actual_tuple = formula_release_tuple(formula_dir / f"{binary}.rb")
        if binary in current and actual_tuple != approved_tuple:
            raise ValueError(
                f"enabled legacy exception {binary} does not match its exact pinned tuple"
            )
        if binary not in current and actual_tuple == approved_tuple:
            raise ValueError(
                f"retired legacy exception {binary} still uses its pinned legacy tuple"
            )
    return current


def verify_transition(
    current_config: Path,
    formula_dir: Path,
    *,
    base_config: Optional[Path],
) -> None:
    current = verify_current_state(current_config, formula_dir)

    if base_config is None:
        expected_bootstrap = frozenset(LEGACY_DIST_RELEASES)
        if current != expected_bootstrap:
            raise ValueError(
                "legacy bootstrap must enable exactly the four hardcoded pinned releases"
            )
        return

    base = load_legacy_exceptions(base_config)
    reactivated = current - base
    if reactivated:
        raise ValueError(
            "legacy exceptions are one-way and cannot be reactivated: "
            f"{sorted(reactivated)}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current-config", required=True, type=Path)
    parser.add_argument("--formula-dir", required=True, type=Path)
    transition = parser.add_mutually_exclusive_group(required=True)
    transition.add_argument("--base-config", type=Path)
    transition.add_argument("--bootstrap", action="store_true")
    args = parser.parse_args()

    try:
        verify_transition(
            args.current_config,
            args.formula_dir,
            base_config=args.base_config if not args.bootstrap else None,
        )
    except ValueError as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
