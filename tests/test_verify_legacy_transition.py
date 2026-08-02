from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.verify_formula_version import LEGACY_DIST_RELEASES
from scripts.verify_legacy_transition import verify_transition


PUBLIC_SHA = "a" * 64


def write_config(path: Path, enabled: set[str]) -> Path:
    path.write_text(
        json.dumps({"enabled": sorted(enabled)}, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def public_tuple(binary: str) -> tuple[str, str, str]:
    version = "1.2.3"
    return (
        version,
        f"https://github.com/bluearchio/{binary}/releases/download/"
        f"v{version}/{binary}-macos-arm64.zip",
        PUBLIC_SHA,
    )


def write_formula(formula_dir: Path, binary: str, release: tuple[str, str, str]) -> None:
    version, url, sha256 = release
    (formula_dir / f"{binary}.rb").write_text(
        f'''class TestFormula < Formula
  url "{url}"
  version "{version}"
  sha256 "{sha256}"
end
''',
        encoding="utf-8",
    )


def write_formulae(formula_dir: Path, enabled: set[str]) -> None:
    formula_dir.mkdir()
    for binary, legacy_tuple in LEGACY_DIST_RELEASES.items():
        release = legacy_tuple if binary in enabled else public_tuple(binary)
        write_formula(formula_dir, binary, release)


class VerifyLegacyTransitionTests(unittest.TestCase):
    def test_allows_exact_initial_bootstrap(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            directory = Path(tmpdir)
            enabled = set(LEGACY_DIST_RELEASES)
            current = write_config(directory / "current.json", enabled)
            formula_dir = directory / "Formula"
            write_formulae(formula_dir, enabled)

            verify_transition(current, formula_dir, base_config=None)

    def test_bootstrap_requires_all_four_exact_pinned_releases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            directory = Path(tmpdir)
            enabled = set(LEGACY_DIST_RELEASES) - {"bluearch-aws-core"}
            current = write_config(directory / "current.json", enabled)
            formula_dir = directory / "Formula"
            write_formulae(formula_dir, enabled)

            with self.assertRaisesRegex(ValueError, "exactly the four"):
                verify_transition(current, formula_dir, base_config=None)

    def test_allows_only_removing_exceptions_from_base(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            directory = Path(tmpdir)
            base_enabled = set(LEGACY_DIST_RELEASES)
            current_enabled = base_enabled - {"bluearch-aws-core"}
            base = write_config(directory / "base.json", base_enabled)
            current = write_config(directory / "current.json", current_enabled)
            formula_dir = directory / "Formula"
            write_formulae(formula_dir, current_enabled)

            verify_transition(current, formula_dir, base_config=base)

    def test_rejects_reactivating_a_removed_exception_and_legacy_formula(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            directory = Path(tmpdir)
            reactivated = {"bluearch-aws-core"}
            base = write_config(directory / "base.json", set())
            current = write_config(directory / "current.json", reactivated)
            formula_dir = directory / "Formula"
            write_formulae(formula_dir, reactivated)

            with self.assertRaisesRegex(ValueError, "cannot be reactivated"):
                verify_transition(current, formula_dir, base_config=base)

    def test_rejects_enabled_exception_without_exact_pinned_formula(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            directory = Path(tmpdir)
            enabled = set(LEGACY_DIST_RELEASES)
            base = write_config(directory / "base.json", enabled)
            current = write_config(directory / "current.json", enabled)
            formula_dir = directory / "Formula"
            write_formulae(formula_dir, enabled)
            write_formula(formula_dir, "bluearch-aws-core", public_tuple("bluearch-aws-core"))

            with self.assertRaisesRegex(ValueError, "does not match"):
                verify_transition(current, formula_dir, base_config=base)

    def test_rejects_retired_exception_still_using_legacy_formula(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            directory = Path(tmpdir)
            base = write_config(directory / "base.json", {"bluearch-aws-core"})
            current = write_config(directory / "current.json", set())
            formula_dir = directory / "Formula"
            write_formulae(formula_dir, set())
            write_formula(
                formula_dir,
                "bluearch-aws-core",
                LEGACY_DIST_RELEASES["bluearch-aws-core"],
            )

            with self.assertRaisesRegex(ValueError, "still uses"):
                verify_transition(current, formula_dir, base_config=base)


if __name__ == "__main__":
    unittest.main()
