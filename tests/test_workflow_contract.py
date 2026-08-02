from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = REPO_ROOT / ".github" / "workflows"


class WorkflowContractTests(unittest.TestCase):
    def test_secret_scan_uses_checksum_verified_license_free_cli(self) -> None:
        workflow = (WORKFLOW_DIR / "secret-scan.yml").read_text(encoding="utf-8")

        self.assertIn('GITLEAKS_VERSION: "8.30.1"', workflow)
        self.assertIn(
            'GITLEAKS_LINUX_X64_SHA256: "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"',
            workflow,
        )
        self.assertIn("https://github.com/gitleaks/gitleaks/releases/download/", workflow)
        self.assertIn("sha256sum -c -", workflow)
        self.assertIn("gitleaks git --redact --verbose .", workflow)
        self.assertLess(workflow.index("sha256sum -c -"), workflow.index("tar -xzf"))
        self.assertNotIn("gitleaks/gitleaks-action", workflow)
        self.assertIn("persist-credentials: false", workflow)

    def test_formula_install_uses_fully_qualified_formula_specific_trust(self) -> None:
        workflow = (WORKFLOW_DIR / "ci.yml").read_text(encoding="utf-8")

        self.assertIn('brew install "$TAP_NAME/bluearch-aws-core"', workflow)
        self.assertIn('brew install "$TAP_NAME/$FORMULA"', workflow)
        self.assertIn('brew tap "$TAP_NAME"', workflow)
        self.assertEqual(workflow.count("fetch-depth: 0"), 3)
        self.assertEqual(
            workflow.count('git -C "$tap_root" fetch --unshallow origin'),
            2,
        )
        self.assertEqual(
            workflow.count(
                'git -C "$tap_root" fetch --no-tags --force "$GITHUB_WORKSPACE" '
                "HEAD:refs/remotes/ci/workspace"
            ),
            2,
        )
        self.assertEqual(
            workflow.count(
                'git -C "$tap_root" checkout --detach refs/remotes/ci/workspace'
            ),
            2,
        )
        self.assertNotIn('brew tap "$TAP_NAME" "$GITHUB_WORKSPACE"', workflow)
        self.assertIn("brew trust --json=v1", workflow)
        self.assertIn('if "bluearchio/tap" in trust["taps"]:', workflow)
        self.assertNotIn('brew trust "$TAP_NAME"', workflow)
        self.assertNotIn("brew trust bluearchio/tap", workflow)

    def test_formula_version_check_uses_exact_public_identity_verifier(self) -> None:
        workflow = (WORKFLOW_DIR / "ci.yml").read_text(encoding="utf-8")

        self.assertIn("scripts/verify_formula_version.py", workflow)
        self.assertIn('--binary "$BINARY"', workflow)
        self.assertIn('--expected "$expected_version"', workflow)
        self.assertIn('--source-url "$source_url"', workflow)
        self.assertIn('--sha256 "$formula_sha256"', workflow)
        self.assertIn(
            "--legacy-exceptions config/legacy-dist-exceptions.json",
            workflow,
        )
        self.assertIn('version_output_file="$RUNNER_TEMP/version-output.txt"', workflow)
        self.assertIn('< "$version_output_file"', workflow)
        self.assertNotIn('version_output="$(HOME=', workflow)
        self.assertNotIn("(?<![0-9])", workflow)

    def test_repository_contract_enforces_monotonic_legacy_transition(self) -> None:
        workflow = (WORKFLOW_DIR / "ci.yml").read_text(encoding="utf-8")

        self.assertIn("scripts/verify_legacy_transition.py", workflow)
        self.assertIn('base_revision="$PR_BASE_SHA"', workflow)
        self.assertIn('base_revision="$PUSH_BEFORE_SHA"', workflow)
        self.assertIn('git cat-file -e "${base_revision}^{commit}"', workflow)
        self.assertIn('git show "${base_revision}:${current_config}"', workflow)
        self.assertIn('"${verify[@]}" --base-config "$base_config"', workflow)
        self.assertIn('"${verify[@]}" --bootstrap', workflow)
        self.assertIn("fetch-depth: 0", workflow)

        repository_contract = workflow[
            workflow.index("  repository-contract:") : workflow.index("  formula-quality:")
        ]
        self.assertIn("scripts/verify_legacy_transition.py", repository_contract)

    def test_required_check_names_are_stable(self) -> None:
        ci = (WORKFLOW_DIR / "ci.yml").read_text(encoding="utf-8")
        codeql = (WORKFLOW_DIR / "codeql.yml").read_text(encoding="utf-8")
        secret_scan = (WORKFLOW_DIR / "secret-scan.yml").read_text(encoding="utf-8")

        self.assertIn("name: Tap release gate", ci)
        self.assertIn("name: Analyze Ruby", codeql)
        self.assertIn("  gitleaks:\n", secret_scan)

    def test_all_checkouts_disable_persisted_credentials(self) -> None:
        for workflow_name in ("ci.yml", "codeql.yml", "secret-scan.yml"):
            with self.subTest(workflow=workflow_name):
                workflow = (WORKFLOW_DIR / workflow_name).read_text(encoding="utf-8")
                checkout_count = workflow.count("uses: actions/checkout@v4")
                persisted_credentials_count = workflow.count("persist-credentials: false")
                self.assertGreater(checkout_count, 0)
                self.assertEqual(persisted_credentials_count, checkout_count)


if __name__ == "__main__":
    unittest.main()
