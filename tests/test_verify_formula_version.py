from __future__ import annotations

import unittest

from scripts.verify_formula_version import verify_version_output


class VerifyFormulaVersionTests(unittest.TestCase):
    def test_accepts_exact_public_identity_variants(self) -> None:
        for binary in (
            "bluearch-aws-core",
            "bluearch-aws-governance",
            "bluearch-aws-ops",
            "bluearch-aws-tags",
        ):
            for suffix in ("1.2.3", "v1.2.3", "1.2.3 (production)"):
                with self.subTest(binary=binary, suffix=suffix):
                    verify_version_output(binary, "1.2.3", f"{binary} {suffix}\n")

    def test_rejects_non_exact_or_legacy_identities(self) -> None:
        invalid = (
            "bluearch-aws-core 1.2.3.1",
            "bluearch-aws-core 1.2.3-closed",
            "bluearch-aws-core 1.2.30",
            "bluearch-core 1.2.3",
            "bluearch-aws-core 1.2.3\nbluearch-aws-core v1.2.3",
        )
        for output in invalid:
            with self.subTest(output=output), self.assertRaises(ValueError):
                verify_version_output("bluearch-aws-core", "1.2.3", output)

    def test_rejects_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            verify_version_output("bluearch-core", "1.2.3", "bluearch-core 1.2.3")
        with self.assertRaises(ValueError):
            verify_version_output("bluearch-aws-core", "v1.2.3", "bluearch-aws-core v1.2.3")


if __name__ == "__main__":
    unittest.main()
