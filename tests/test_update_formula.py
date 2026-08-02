from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
UPDATE_SCRIPT = REPO_ROOT / "scripts" / "update_formula.py"
SHA256 = "a" * 64
PUBLIC_PACKAGES = (
    "bluearch-aws-core",
    "bluearch-aws-governance",
    "bluearch-aws-ops",
    "bluearch-aws-tags",
)


def sample_formula() -> str:
    return '''class BluearchAwsCore < Formula
  desc "Test formula"
  homepage "https://github.com/bluearchio/bluearch-aws-core"
  url "https://example.invalid/old.zip"
  version "0.0.1"
  sha256 "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
  license "MIT"
  disable! date: "2026-01-01", because: "waiting for a public release"

  def install
    bin.install "old-command"
  end

  def caveats
    <<~EOS
      Preserve this text exactly.
      bluearch-aws-governance catalog import
    EOS
  end
end
'''


class UpdateFormulaTests(unittest.TestCase):
    def write_exception_config(
        self,
        directory: Path,
        enabled: tuple[str, ...] = PUBLIC_PACKAGES,
    ) -> Path:
        config = directory / "legacy-dist-exceptions.json"
        config.write_text(json.dumps({"enabled": list(enabled)}, indent=2) + "\n", encoding="utf-8")
        return config

    def run_update(
        self,
        formula: Path,
        legacy_exceptions: Path,
        **overrides: str,
    ) -> subprocess.CompletedProcess[str]:
        values = {
            "repo": "bluearchio/bluearch-aws-core",
            "version": "v1.2.3",
            "asset": "bluearch-aws-core-macos-arm64.zip",
            "sha256": SHA256,
            "binary": "bluearch-aws-core",
        }
        values.update(overrides)
        return subprocess.run(
            [
                sys.executable,
                str(UPDATE_SCRIPT),
                "--formula",
                str(formula),
                "--repo",
                values["repo"],
                "--version",
                values["version"],
                "--asset",
                values["asset"],
                "--sha256",
                values["sha256"],
                "--binary",
                values["binary"],
                "--legacy-exceptions",
                str(legacy_exceptions),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_updates_only_release_metadata_and_install_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            directory = Path(tmpdir)
            formula = directory / "bluearch-aws-core.rb"
            legacy_exceptions = self.write_exception_config(
                directory,
                tuple(reversed(PUBLIC_PACKAGES)),
            )
            original = sample_formula()
            original_caveats = original[original.index("  def caveats") :]
            formula.write_text(original, encoding="utf-8")

            result = self.run_update(formula, legacy_exceptions)

            self.assertEqual(result.returncode, 0, result.stderr)
            updated = formula.read_text(encoding="utf-8")
            expected_url = (
                "https://github.com/bluearchio/bluearch-aws-core/releases/download/"
                "v1.2.3/bluearch-aws-core-macos-arm64.zip"
            )
            self.assertIn(f'  url "{expected_url}"', updated)
            self.assertNotIn("/latest/", updated)
            self.assertIn('  version "1.2.3"', updated)
            self.assertIn(f'  sha256 "{SHA256}"', updated)
            self.assertIn('    bin.install "bluearch-aws-core"', updated)
            self.assertNotIn("disable!", updated)
            self.assertEqual(updated[updated.index("  def caveats") :], original_caveats)
            self.assertEqual(
                json.loads(legacy_exceptions.read_text(encoding="utf-8")),
                {
                    "enabled": [
                        "bluearch-aws-governance",
                        "bluearch-aws-ops",
                        "bluearch-aws-tags",
                    ]
                },
            )

    def test_rejects_prerelease_and_build_tags_without_writing(self) -> None:
        for version in (
            "v1.2.3-rc.1",
            "v1.2.3+build.7",
            "v1.2.3-rc.1+build.7",
        ):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as tmpdir:
                directory = Path(tmpdir)
                formula = directory / "bluearch-aws-core.rb"
                legacy_exceptions = self.write_exception_config(
                    directory,
                    ("bluearch-aws-core",),
                )
                original_formula = sample_formula()
                original_exceptions = legacy_exceptions.read_text(encoding="utf-8")
                formula.write_text(original_formula, encoding="utf-8")

                result = self.run_update(
                    formula,
                    legacy_exceptions,
                    version=version,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("stable v-prefixed semantic version", result.stderr)
                self.assertEqual(formula.read_text(encoding="utf-8"), original_formula)
                self.assertEqual(
                    legacy_exceptions.read_text(encoding="utf-8"),
                    original_exceptions,
                )

    def test_rejects_inputs_outside_the_public_release_contract(self) -> None:
        invalid_inputs = (
            {"binary": "bluearch-core"},
            {"repo": "bluearchio/bluearch-aws-core/extra"},
            {"repo": 'bluearchio/bluearch-aws-core"\nsystem "false"'},
            {"version": "v1.2.3/../../latest"},
            {"version": "1.2.3"},
            {"asset": "bluearch-core-macos-arm64.zip"},
            {"sha256": "A" * 64},
            {"sha256": "a" * 63},
        )

        for overrides in invalid_inputs:
            with self.subTest(overrides=overrides), tempfile.TemporaryDirectory() as tmpdir:
                formula = Path(tmpdir) / "bluearch-aws-core.rb"
                legacy_exceptions = self.write_exception_config(Path(tmpdir))
                original = sample_formula()
                formula.write_text(original, encoding="utf-8")
                original_exceptions = legacy_exceptions.read_text(encoding="utf-8")

                result = self.run_update(formula, legacy_exceptions, **overrides)

                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(formula.read_text(encoding="utf-8"), original)
                self.assertEqual(legacy_exceptions.read_text(encoding="utf-8"), original_exceptions)

    def test_rejects_formula_filename_that_does_not_match_binary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            directory = Path(tmpdir)
            formula = directory / "different.rb"
            legacy_exceptions = self.write_exception_config(directory)
            original = sample_formula()
            formula.write_text(original, encoding="utf-8")

            result = self.run_update(formula, legacy_exceptions)

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(formula.read_text(encoding="utf-8"), original)

    def test_rejects_duplicate_or_missing_formula_fields_without_writing(self) -> None:
        required_lines = (
            '  url "https://example.invalid/old.zip"',
            '  version "0.0.1"',
            '  sha256 "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"',
            '    bin.install "old-command"',
        )

        for required_line in required_lines:
            for mutation in ("duplicate", "missing"):
                with (
                    self.subTest(required_line=required_line, mutation=mutation),
                    tempfile.TemporaryDirectory() as tmpdir,
                ):
                    formula = Path(tmpdir) / "bluearch-aws-core.rb"
                    legacy_exceptions = self.write_exception_config(Path(tmpdir))
                    if mutation == "duplicate":
                        replacement = f"{required_line}\n{required_line}"
                    else:
                        replacement = ""
                    original = sample_formula().replace(required_line, replacement)
                    formula.write_text(original, encoding="utf-8")

                    result = self.run_update(formula, legacy_exceptions)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(formula.read_text(encoding="utf-8"), original)

    def test_rejects_arbitrary_or_malformed_exception_configs(self) -> None:
        invalid_documents = (
            {"enabled": ["bluearch-core"]},
            {"enabled": ["bluearch-aws-core", "bluearch-aws-core"]},
            {"enabled": "bluearch-aws-core"},
            {"enabled": [], "unexpected": []},
            ["bluearch-aws-core"],
        )

        for document in invalid_documents:
            with self.subTest(document=document), tempfile.TemporaryDirectory() as tmpdir:
                directory = Path(tmpdir)
                formula = directory / "bluearch-aws-core.rb"
                original_formula = sample_formula()
                formula.write_text(original_formula, encoding="utf-8")
                legacy_exceptions = directory / "legacy-dist-exceptions.json"
                original_config = json.dumps(document, indent=2) + "\n"
                legacy_exceptions.write_text(original_config, encoding="utf-8")

                result = self.run_update(formula, legacy_exceptions)

                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(formula.read_text(encoding="utf-8"), original_formula)
                self.assertEqual(legacy_exceptions.read_text(encoding="utf-8"), original_config)


if __name__ == "__main__":
    unittest.main()
