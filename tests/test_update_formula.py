from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
UPDATE_SCRIPT = REPO_ROOT / "scripts" / "update_formula.py"
SHA256 = "a" * 64


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
    def run_update(self, formula: Path, **overrides: str) -> subprocess.CompletedProcess[str]:
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
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_updates_only_release_metadata_and_install_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            formula = Path(tmpdir) / "bluearch-aws-core.rb"
            original = sample_formula()
            original_caveats = original[original.index("  def caveats") :]
            formula.write_text(original, encoding="utf-8")

            result = self.run_update(formula)

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

    def test_accepts_well_formed_prerelease_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            formula = Path(tmpdir) / "bluearch-aws-core.rb"
            formula.write_text(sample_formula(), encoding="utf-8")

            result = self.run_update(formula, version="v1.2.3-rc.1+build.7")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(
                "/releases/download/v1.2.3-rc.1+build.7/",
                formula.read_text(encoding="utf-8"),
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
                original = sample_formula()
                formula.write_text(original, encoding="utf-8")

                result = self.run_update(formula, **overrides)

                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(formula.read_text(encoding="utf-8"), original)

    def test_rejects_formula_filename_that_does_not_match_binary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            formula = Path(tmpdir) / "different.rb"
            original = sample_formula()
            formula.write_text(original, encoding="utf-8")

            result = self.run_update(formula)

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
                    if mutation == "duplicate":
                        replacement = f"{required_line}\n{required_line}"
                    else:
                        replacement = ""
                    original = sample_formula().replace(required_line, replacement)
                    formula.write_text(original, encoding="utf-8")

                    result = self.run_update(formula)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(formula.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
