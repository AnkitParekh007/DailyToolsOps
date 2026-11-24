"""Prevent regressions in published repository URLs."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class RepositoryIdentityTests(unittest.TestCase):
    def test_canonical_links(self):
        for path in [ROOT / "README.md", ROOT / "website/index.html", ROOT / "website/app.js", ROOT / "website/README.md", *ROOT.glob("packs/**/INSTRUCTIONS.md"), *ROOT.glob("packs/**/README.md")]:
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                self.assertNotIn("AnkitParekh007/" + "daily-tools-resources", content)
                self.assertNotIn("ankitparekh007.github.io/" + "daily-tools-resources", content)
        self.assertIn("https://github.com/AnkitParekh007/DailyToolsOps", (ROOT / "website/index.html").read_text(encoding="utf-8"))
        self.assertIn("https://ankitparekh007.github.io/DailyToolsOps/", (ROOT / "README.md").read_text(encoding="utf-8"))
