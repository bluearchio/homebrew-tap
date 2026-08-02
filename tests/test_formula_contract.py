from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FORMULA_DIR = REPO_ROOT / "Formula"
PUBLIC_PACKAGES = (
    "bluearch-aws-core",
    "bluearch-aws-governance",
    "bluearch-aws-ops",
    "bluearch-aws-tags",
)
LEGACY_EXECUTABLES = (
    "bluearch",
    "bluearch-core",
    "cloud-governance",
    "tag-manager",
)


def capture(pattern: str, text: str, label: str) -> str:
    matches = re.findall(pattern, text, re.MULTILINE)
    if len(matches) != 1:
        raise AssertionError(f"expected exactly one {label}, found {len(matches)}")
    return matches[0]


class FormulaContractTests(unittest.TestCase):
    def test_tap_contains_exactly_the_four_public_formulae(self) -> None:
        names = tuple(sorted(path.stem for path in FORMULA_DIR.glob("*.rb")))
        self.assertEqual(names, PUBLIC_PACKAGES)

    def test_formulae_install_and_test_only_the_public_executables(self) -> None:
        for package in PUBLIC_PACKAGES:
            with self.subTest(package=package):
                text = (FORMULA_DIR / f"{package}.rb").read_text(encoding="utf-8")
                installed = capture(r'^\s+bin\.install "([^"]+)"$', text, "install target")
                tested = capture(
                    r'^\s+system "#\{bin\}/([^"]+)", "--version"$',
                    text,
                    "version test target",
                )
                self.assertEqual(installed, package)
                self.assertEqual(tested, package)

                for legacy in LEGACY_EXECUTABLES:
                    self.assertNotRegex(text, rf'bin\.install "{re.escape(legacy)}"')
                    self.assertNotRegex(text, rf'#\{{bin\}}/{re.escape(legacy)}(?:"|\s)')

    def test_urls_versions_and_checksums_are_immutable_and_consistent(self) -> None:
        for package in PUBLIC_PACKAGES:
            with self.subTest(package=package):
                text = (FORMULA_DIR / f"{package}.rb").read_text(encoding="utf-8")
                url = capture(r'^\s+url "([^"]+)"$', text, "URL")
                version = capture(r'^\s+version "([^"]+)"$', text, "version")
                sha256 = capture(r'^\s+sha256 "([^"]+)"$', text, "SHA256")
                asset = f"{package}-macos-arm64.zip"
                release_tag = f"v{version}"
                allowed_urls = {
                    f"https://dist.bluearch.io/releases/{package}/{release_tag}/{asset}",
                    f"https://github.com/bluearchio/{package}/releases/download/{release_tag}/{asset}",
                }

                self.assertRegex(version, r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
                self.assertIn(url, allowed_urls)
                self.assertNotIn("/latest/", url)
                self.assertRegex(sha256, r"^[0-9a-f]{64}$")

    def test_products_depend_on_public_core_formula(self) -> None:
        for package in PUBLIC_PACKAGES:
            with self.subTest(package=package):
                text = (FORMULA_DIR / f"{package}.rb").read_text(encoding="utf-8")
                dependencies = re.findall(r'^\s+depends_on "([^"]+)"$', text, re.MULTILINE)
                if package == "bluearch-aws-core":
                    self.assertNotIn("bluearch-aws-core", dependencies)
                else:
                    self.assertEqual(dependencies, ["bluearch-aws-core"])

    def test_governance_caveat_uses_registered_catalog_command(self) -> None:
        text = (FORMULA_DIR / "bluearch-aws-governance.rb").read_text(encoding="utf-8")
        self.assertIn("bluearch-aws-governance catalog import", text)
        self.assertNotIn("bluearch-aws-governance catalog load", text)


if __name__ == "__main__":
    unittest.main()
