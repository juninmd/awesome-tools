#!/usr/bin/env python3
"""
Security Tests for awesome-tools repository.

This module validates security measures including:
- .gitignore configuration
- Secret scanning patterns
- Security documentation presence
"""

import os
import re
import subprocess
import unittest
from pathlib import Path


class TestGitignoreSecurity(unittest.TestCase):
    """Test .gitignore file contains required security patterns."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo_root = Path(__file__).parent.parent
        self.gitignore_path = self.repo_root / ".gitignore"

    def test_gitignore_exists(self):
        """Verify .gitignore file exists."""
        self.assertTrue(
            self.gitignore_path.exists(),
            ".gitignore file must exist in repository root"
        )

    def test_gitignore_contains_env_patterns(self):
        """Verify .gitignore contains environment file patterns."""
        content = self.gitignore_path.read_text()
        required_patterns = [
            ".env",
            ".env.local",
            ".env.*.local",
        ]
        for pattern in required_patterns:
            self.assertIn(
                pattern,
                content,
                f".gitignore must exclude {pattern}"
            )

    def test_gitignore_contains_key_patterns(self):
        """Verify .gitignore contains private key patterns."""
        content = self.gitignore_path.read_text()
        required_patterns = [
            "*.key",
            "*.pem",
            "*.p12",
        ]
        for pattern in required_patterns:
            self.assertIn(
                pattern,
                content,
                f".gitignore must exclude {pattern}"
            )

    def test_gitignore_contains_secrets_directory(self):
        """Verify .gitignore contains secrets directory pattern."""
        content = self.gitignore_path.read_text()
        self.assertIn(
            "secrets/",
            content,
            ".gitignore must exclude secrets/ directory"
        )


class TestSecretScanning(unittest.TestCase):
    """Test for accidentally committed secrets."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo_root = Path(__file__).parent.parent
        self.common_secret_patterns = [
            r'AKIA[0-9A-Z]{16}',  # AWS Access Key
            r'ghp_[0-9a-zA-Z]{36}',  # GitHub Personal Access Token
            r'sk_live_[0-9a-zA-Z]{24}',  # Stripe Live Secret Key
            r'sk_test_[0-9a-zA-Z]{24}',  # Stripe Test Secret Key
            r'password\s*=\s*["\'][^"\']+["\']',  # Hardcoded passwords
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',  # Hardcoded API keys
        ]

    def _scan_file_for_secrets(self, file_path):
        """Scan a file for potential secrets."""
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
                self.assertEqual(
                    len(aws_secrets),
                    0,
                    f"AWS keys found in {file_path}"
                )

    def test_no_github_tokens_committed(self):
        """Verify no GitHub tokens are committed."""
        for file_path in self.repo_root.rglob("*"):
            if file_path.is_file() and ".git" not in str(file_path):
                secrets = self._scan_file_for_secrets(file_path)
                gh_secrets = [s for s in secrets if s.startswith("ghp_")]
                self.assertEqual(
                    len(gh_secrets),
                    0,
                    f"GitHub tokens found in {file_path}"
                )


class TestSecurityDocumentation(unittest.TestCase):
    """Test security documentation presence and completeness."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo_root = Path(__file__).parent.parent

    def test_security_md_exists(self):
        """Verify SECURITY.md file exists."""
        security_md = self.repo_root / "SECURITY.md"
        self.assertTrue(
            security_md.exists(),
            "SECURITY.md must exist in repository root"
        )

    def test_security_md_has_content(self):
        """Verify SECURITY.md has meaningful content."""
        security_md = self.repo_root / "SECURITY.md"
        if security_md.exists():
            content = security_md.read_text()
            self.assertGreater(
                len(content),
                100,
                "SECURITY.md must have substantial content"
            )

    def test_security_md_covers_owasp(self):
        """Verify SECURITY.md references OWASP Top 10."""
        security_md = self.repo_root / "SECURITY.md"
        if security_md.exists():
            content = security_md.read_text()
            self.assertIn(
                "OWASP",
                content,
                "SECURITY.md must reference OWASP Top 10"
            )


class TestDependabotConfiguration(unittest.TestCase):
    """Test Dependabot configuration for automated dependency updates."""

    def setUp(self):
        """Set up test fixtures."""
        self.repo_root = Path(__file__).parent.parent

    def test_dependabot_yml_exists(self):
        """Verify .github/dependabot.yml exists."""
        dependabot_path = self.repo_root / ".github" / "dependabot.yml"
        self.assertTrue(
            dependabot_path.exists(),
            ".github/dependabot.yml must exist"
        )

    def test_dependabot_has_github_actions(self):
        """Verify Dependabot monitors GitHub Actions."""
        dependabot_path = self.repo_root / ".github" / "dependabot.yml"
        if dependabot_path.exists():
            content = dependabot_path.read_text()
            self.assertIn(
                "github-actions",
                content,
                "Dependabot must monitor github-actions ecosystem"
            )

    def test_dependabot_has_schedule(self):
        """Verify Dependabot has a schedule configured."""
        dependabot_path = self.repo_root / ".github" / "dependabot.yml"
        if dependabot_path.exists():
            content = dependabot_path.read_text()
            self.assertIn(
                "schedule",
                content,
                "Dependabot must have a schedule configured"
            )


if __name__ == "__main__":
    unittest.main()
