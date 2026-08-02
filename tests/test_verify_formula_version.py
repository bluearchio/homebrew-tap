from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

from scripts.verify_formula_version import (
    LEGACY_DIST_RELEASES,
    load_legacy_exceptions,
    verify_version_output,
)


PUBLIC_SHA = "a" * 64
REPO_ROOT = Path(__file__).resolve().parents[1]
LEGACY_CONFIG = REPO_ROOT / "config" / "legacy-dist-exceptions.json"


def github_url(binary: str, version: str = "1.2.3") -> str:
    return (
        f"https://github.com/bluearchio/{binary}/releases/download/"
        f"v{version}/{binary}-macos-arm64.zip"
    )


def write_config(directory: Path, enabled: list[str]) -> Path:
    config = directory / "legacy-dist-exceptions.json"
    config.write_text(json.dumps({"enabled": enabled}, indent=2) + "\n", encoding="utf-8")
    return config


class VerifyFormulaVersionTests(unittest.TestCase):
    def test_accepts_exact_public_identity_variants(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = write_config(Path(tmpdir), [])
            for binary in LEGACY_DIST_RELEASES:
                for suffix in ("1.2.3", "v1.2.3", "1.2.3 (production)"):
                    with self.subTest(binary=binary, suffix=suffix):
                        verify_version_output(
                            binary,
                            "1.2.3",
                            github_url(binary),
                            PUBLIC_SHA,
                            f"{binary} {suffix}\n",
                            config,
                        )

    def test_rejects_non_exact_or_legacy_identities(self) -> None:
        invalid = (
            "bluearch-aws-core 1.2.3.1",
            "bluearch-aws-core 1.2.3-closed",
            "bluearch-aws-core 1.2.30",
            "bluearch-core 1.2.3",
            "bluearch-aws-core 1.2.3\nbluearch-aws-core v1.2.3",
            "bluearch-aws-core 1.2.3\nbluearch-core 1.2.3",
            "bluearch-aws-core 1.2.3\nbluearch-aws-core 9.9.9",
            "bluearch-aws-core 1.2.3\nbluearch-aws-core 1.2.3-closed",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            config = write_config(Path(tmpdir), ["bluearch-aws-core"])
            for output in invalid:
                with self.subTest(output=output), self.assertRaises(ValueError):
                    verify_version_output(
                        "bluearch-aws-core",
                        "1.2.3",
                        github_url("bluearch-aws-core"),
                        PUBLIC_SHA,
                        output,
                        config,
                    )

    def test_allows_only_the_four_exact_pinned_legacy_dist_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = write_config(Path(tmpdir), list(LEGACY_DIST_RELEASES))
            for binary, (version, source_url, sha256) in LEGACY_DIST_RELEASES.items():
                with self.subTest(binary=binary):
                    verify_version_output(
                        binary,
                        version,
                        source_url,
                        sha256,
                        "legacy output\n",
                        config,
                    )
                    with self.assertRaises(ValueError):
                        verify_version_output(
                            binary,
                            version,
                            source_url,
                            "b" * 64,
                            "legacy output\n",
                            config,
                        )
                    with self.assertRaises(ValueError):
                        verify_version_output(
                            binary,
                            version,
                            source_url.replace("dist.bluearch.io", "mirror.example"),
                            sha256,
                            "legacy output\n",
                            config,
                        )

    def test_enabled_config_entries_match_only_exact_current_dist_formulae(self) -> None:
        enabled = load_legacy_exceptions(LEGACY_CONFIG)

        for binary, approved_tuple in LEGACY_DIST_RELEASES.items():
            with self.subTest(binary=binary):
                formula = (REPO_ROOT / "Formula" / f"{binary}.rb").read_text(encoding="utf-8")
                actual_tuple = tuple(
                    re.search(pattern, formula, re.MULTILINE).group(1)
                    for pattern in (
                        r'^\s+version "([^"]+)"$',
                        r'^\s+url "([^"]+)"$',
                        r'^\s+sha256 "([^"]+)"$',
                    )
                )
                if binary in enabled:
                    self.assertEqual(actual_tuple, approved_tuple)
                else:
                    self.assertNotEqual(actual_tuple, approved_tuple)

    def test_removed_exception_makes_legacy_rollback_fail(self) -> None:
        binary = "bluearch-aws-core"
        version, source_url, sha256 = LEGACY_DIST_RELEASES[binary]
        with tempfile.TemporaryDirectory() as tmpdir:
            config = write_config(Path(tmpdir), [])
            with self.assertRaises(ValueError):
                verify_version_output(
                    binary,
                    version,
                    source_url,
                    sha256,
                    "bluearch-core 0.2.5\n",
                    config,
                )

    def test_rejects_arbitrary_exception_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = write_config(Path(tmpdir), ["bluearch-core"])
            with self.assertRaises(ValueError):
                load_legacy_exceptions(config)

    def test_rejects_invalid_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = write_config(Path(tmpdir), [])
            with self.assertRaises(ValueError):
                verify_version_output(
                    "bluearch-core",
                    "1.2.3",
                    github_url("bluearch-core"),
                    PUBLIC_SHA,
                    "bluearch-core 1.2.3",
                    config,
                )
            with self.assertRaises(ValueError):
                verify_version_output(
                    "bluearch-aws-core",
                    "v1.2.3",
                    github_url("bluearch-aws-core"),
                    PUBLIC_SHA,
                    "bluearch-aws-core v1.2.3",
                    config,
                )


if __name__ == "__main__":
    unittest.main()
