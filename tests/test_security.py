#!/usr/bin/env python3
"""
Security Tests for awesome-tools repository.

This module validates security measures including:
- .gitignore configuration
- Secret scanning patterns
- Security documentation presence
- GitHub Workflows Action pinning by SHA
"""

import re
import unittest
from pathlib import Path


class TestGitignoreSecurity(unittest.TestCase):
    """Test .gitignore file contains required security patterns."""

    def setUp(self):
        self.repo_root = Path(__file__).parent.parent
        self.gitignore_path = self.repo_root / ".gitignore"

    def test_gitignore_exists(self):
        """Verify .gitignore file exists."""
        self.assertTrue(self.gitignore_path.exists(), ".gitignore file must exist")

    def test_gitignore_contains_env_patterns(self):
        """Verify .gitignore contains environment file patterns."""
        content = self.gitignore_path.read_text()
        for pattern in [".env", ".env.local", ".env.*.local"]:
            self.assertIn(pattern, content, f".gitignore must exclude {pattern}")

    def test_gitignore_contains_key_patterns(self):
        """Verify .gitignore contains private key patterns."""
        content = self.gitignore_path.read_text()
        for pattern in ["*.key", "*.pem", "*.p12"]:
            self.assertIn(pattern, content, f".gitignore must exclude {pattern}")

    def test_gitignore_contains_secrets_directory(self):
        """Verify .gitignore contains secrets directory pattern."""
        content = self.gitignore_path.read_text()
        self.assertIn("secrets/", content, ".gitignore must exclude secrets/ directory")


class TestSecretScanning(unittest.TestCase):
    """Test for accidentally committed secrets."""

    def setUp(self):
        self.repo_root = Path(__file__).parent.parent
        self.common_secret_patterns = [
            r'AKIA[0-9A-Z]{16}',
            r'ghp_[0-9a-zA-Z]{36}',
            r'sk_live_[0-9a-zA-Z]{24}',
            r'sk_test_[0-9a-zA-Z]{24}',
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
        ]

    def _scan_file_for_secrets(self, file_path):
        try:
            content = file_path.read_text(errors='ignore')
            found_secrets = []
            for pattern in self.common_secret_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    found_secrets.extend(matches)
            return found_secrets
        except Exception:
            return []

    def test_no_aws_keys_committed(self):
        """Verify no AWS access keys are committed."""
        for file_path in self.repo_root.rglob("*"):
            if file_path.is_file() and ".git" not in str(file_path):
                secrets = self._scan_file_for_secrets(file_path)
                aws_secrets = [s for s in secrets if s.startswith("AKIA")]
                self.assertEqual(len(aws_secrets), 0, f"AWS keys found in {file_path}")

    def test_no_github_tokens_committed(self):
        """Verify no GitHub tokens are committed."""
        for file_path in self.repo_root.rglob("*"):
            if file_path.is_file() and ".git" not in str(file_path):
                secrets = self._scan_file_for_secrets(file_path)
                gh_secrets = [s for s in secrets if s.startswith("ghp_")]
                self.assertEqual(len(gh_secrets), 0, f"GitHub tokens found in {file_path}")


class TestSecurityDocumentation(unittest.TestCase):
    """Test security documentation presence and completeness."""

    def setUp(self):
        self.repo_root = Path(__file__).parent.parent

    def test_security_md_exists(self):
        """Verify SECURITY.md file exists."""
        security_md = self.repo_root / "SECURITY.md"
        self.assertTrue(security_md.exists(), "SECURITY.md must exist in repository root")

    def test_security_md_has_content(self):
        """Verify SECURITY.md has meaningful content."""
        security_md = self.repo_root / "SECURITY.md"
        if security_md.exists():
            content = security_md.read_text()
            self.assertGreater(len(content), 100, "SECURITY.md must have substantial content")

    def test_security_md_covers_owasp(self):
        """Verify SECURITY.md references OWASP Top 10."""
        security_md = self.repo_root / "SECURITY.md"
        if security_md.exists():
            content = security_md.read_text()
            self.assertIn("OWASP", content, "SECURITY.md must reference OWASP Top 10")


class TestDependabotConfiguration(unittest.TestCase):
    """Test Dependabot configuration for automated dependency updates."""

    def setUp(self):
        self.repo_root = Path(__file__).parent.parent

    def test_dependabot_yml_exists(self):
        """Verify .github/dependabot.yml exists."""
        dependabot_path = self.repo_root / ".github" / "dependabot.yml"
        self.assertTrue(dependabot_path.exists(), ".github/dependabot.yml must exist")

    def test_dependabot_has_github_actions(self):
        """Verify Dependabot monitors GitHub Actions."""
        dependabot_path = self.repo_root / ".github" / "dependabot.yml"
        if dependabot_path.exists():
            content = dependabot_path.read_text()
            self.assertIn("github-actions", content, "Dependabot must monitor github-actions")

    def test_dependabot_has_schedule(self):
        """Verify Dependabot has a schedule configured."""
        dependabot_path = self.repo_root / ".github" / "dependabot.yml"
        if dependabot_path.exists():
            content = dependabot_path.read_text()
            self.assertIn("schedule", content, "Dependabot must have schedule")


class TestWorkflowPinning(unittest.TestCase):
    """Test that all GitHub Action references are pinned to full commit SHAs."""

    def setUp(self):
        self.repo_root = Path(__file__).parent.parent
        self.workflows_dir = self.repo_root / ".github" / "workflows"

    def _find_unpinned_uses(self, content):
        unpinned = []
        for line in content.splitlines():
            match = re.search(r'uses:\s*(\S+)', line)
            if match:
                ref = match.group(1)
                if not ref.startswith('./'):
                    if not re.search(r'@[0-9a-f]{40}', ref):
                        unpinned.append(ref)
        return unpinned

    def test_all_workflows_pinned(self):
        """Verify all external actions in workflow files are pinned to 40-char SHA."""
        workflow_files = list(self.workflows_dir.glob("*.yml")) + list(self.workflows_dir.glob("*.yaml"))
        self.assertTrue(len(workflow_files) > 0, "No workflow files found")
        for wf in workflow_files:
            content = wf.read_text()
            unpinned = self._find_unpinned_uses(content)
            self.assertEqual(unpinned, [], f"Unpinned action(s) found in {wf.name}: {unpinned}")

    def test_unpinned_action_fails(self):
        """Verify synthetic unpinned action uses (e.g. @main or @v1) fail pinning check."""
        sample_unpinned = "  uses: owner/repo@main\n  uses: actions/checkout@v7"
        unpinned = self._find_unpinned_uses(sample_unpinned)
        self.assertEqual(len(unpinned), 2)
        sample_pinned = "  uses: owner/repo@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7"
        self.assertEqual(len(self._find_unpinned_uses(sample_pinned)), 0)


class TestAgentsDocumentation(unittest.TestCase):
    """Test AGENTS.md guidelines file."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo_root = Path(__file__).parent.parent
        self.agents_md_path = self.repo_root / "AGENTS.md"

    def test_agents_md_exists(self):
        """Verify AGENTS.md exists."""
        self.assertTrue(
            self.agents_md_path.exists(),
            "AGENTS.md file must exist in repository root"
        )

    def test_agents_md_does_not_start_with_code_fence(self):
        """Verify AGENTS.md does not start with a markdown code fence."""
        content = self.agents_md_path.read_text(encoding="utf-8").lstrip()
        self.assertFalse(
            content.startswith("```"),
            "AGENTS.md must not start with a code fence"
        )

    def test_agents_md_mentions_pytest(self):
        """Verify AGENTS.md mentions pytest."""
        content = self.agents_md_path.read_text(encoding="utf-8")
        self.assertIn(
            "pytest",
            content,
            "AGENTS.md must mention pytest"
        )


if __name__ == "__main__":
    unittest.main()
