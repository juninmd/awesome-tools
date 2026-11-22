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
import subprocess
import tempfile
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


SECRET_PATTERNS = {
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "github_token": re.compile(r"ghp_[0-9a-zA-Z]{36}"),
    "stripe_live_key": re.compile(r"sk_live_[0-9a-zA-Z]{24}"),
    "stripe_test_key": re.compile(r"sk_test_[0-9a-zA-Z]{24}"),
    "hardcoded_password": re.compile(r"password\s*=\s*[\"'][^\"']+[\"']", re.IGNORECASE),
    "hardcoded_api_key": re.compile(r"api[_-]?key\s*=\s*[\"'][^\"']+[\"']", re.IGNORECASE),
}
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".pyc"}


def find_secrets(text):
    """(pattern name, line number, masked match) for every hit; the value is never returned in full."""
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for name, pattern in SECRET_PATTERNS.items():
            for match in pattern.finditer(line):
                hits.append((name, lineno, match.group(0)[:4] + "***"))
    return hits


def tracked_text_files(repo_root):
    """Every text file git tracks, so a local .venv or build output never counts as committed."""
    listed = subprocess.run(
        ["git", "ls-files", "-z"], cwd=repo_root, capture_output=True, check=True, text=True
    ).stdout
    for name in filter(None, listed.split("\0")):
        path = repo_root / name
        if path.is_file() and path.suffix.lower() not in BINARY_SUFFIXES:
            yield path


class TestSecretScanning(unittest.TestCase):
    """Test for accidentally committed secrets."""

    @classmethod
    def setUpClass(cls):
        repo_root = Path(__file__).parent.parent
        # Single pass over the repository; unreadable files raise instead of counting as clean
        cls.findings = {}
        for path in tracked_text_files(repo_root):
            hits = find_secrets(path.read_text(errors="ignore"))
            if hits:
                cls.findings[str(path.relative_to(repo_root))] = hits

    def test_no_secrets_committed(self):
        """Verify no known secret pattern is committed (reports file, line and masked value)."""
        for name in SECRET_PATTERNS:
            with self.subTest(pattern=name):
                found = [
                    f"{path}:{lineno} {masked}"
                    for path, hits in self.findings.items()
                    for hit, lineno, masked in hits
                    if hit == name
                ]
                self.assertEqual(found, [], f"{name} found")

    def test_every_pattern_detects_a_synthetic_secret(self):
        """Fixtures are built at runtime so they do not trip push protection or trufflehog."""
        samples = {
            "aws_access_key": "AKIA" + "A" * 16,
            "github_token": "ghp_" + "a" * 36,
            "stripe_live_key": "sk_" + "live_" + "A" * 24,
            "stripe_test_key": "sk_" + "test_" + "A" * 24,
            "hardcoded_password": "pass" + 'word = "hunter2"',
            "hardcoded_api_key": "API_" + "KEY='abc123'",
        }
        self.assertEqual(set(samples), set(SECRET_PATTERNS))
        for name, sample in samples.items():
            with self.subTest(pattern=name):
                self.assertEqual([h[0] for h in find_secrets(sample)], [name])

    def test_innocent_text_is_clean(self):
        self.assertEqual(find_secrets("Use uma variavel de ambiente para a senha e a chave de API."), [])

    def test_untracked_files_are_not_scanned(self):
        """A secret inside a local virtualenv is not a committed secret; a tracked file is."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "tracked.py").write_text("x = 1\n")
            (root / ".venv").mkdir()
            (root / ".venv" / "mod.py").write_text("pass" + 'word = "hunter2"\n')
            subprocess.run(["git", "add", "tracked.py"], cwd=root, check=True)
            self.assertEqual([p.name for p in tracked_text_files(root)], ["tracked.py"])

    def test_report_masks_the_secret(self):
        (hit,) = find_secrets("token: " + "ghp_" + "z" * 36)
        self.assertEqual(hit, ("github_token", 1, "ghp_***"))


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
