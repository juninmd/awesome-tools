"""Catalog integrity: every table row is a unique https link with a description."""

import re
import unittest
from pathlib import Path

README = Path(__file__).parent.parent / "README.md"
ROW = re.compile(r"^\| \[([^\]]+)\]\(([^)]+)\) \| (.+) \|$")


def catalog_rows():
    """Yield (line_no, line) for table rows outside code fences, skipping headers."""
    in_fence = False
    for number, line in enumerate(README.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("| [") and not line.startswith("| [x]"):
            yield number, line


class TestCatalog(unittest.TestCase):
    def test_rows_have_name_url_and_description(self):
        for number, line in catalog_rows():
            self.assertRegex(line, ROW, f"README.md:{number} is not '| [Name](url) | description |'")

    def test_links_use_https(self):
        for number, line in catalog_rows():
            url = ROW.match(line).group(2)
            self.assertTrue(url.startswith("https://"), f"README.md:{number} uses a non-https link: {url}")

    def test_no_duplicate_urls(self):
        seen = {}
        for number, line in catalog_rows():
            url = ROW.match(line).group(2).rstrip("/").lower()
            self.assertNotIn(url, seen, f"README.md:{number} repeats the URL from line {seen.get(url)}")
            seen[url] = number

    def test_catalog_is_not_empty(self):
        self.assertGreater(len(list(catalog_rows())), 30)


if __name__ == "__main__":
    unittest.main()
