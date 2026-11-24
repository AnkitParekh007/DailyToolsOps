import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
class SiteTests(unittest.TestCase):
    def test_downloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "site"
            subprocess.run([sys.executable, str(ROOT / "scripts/build_site.py"), str(out)], check=True)
            self.assertTrue((out / "index.html").is_file())
            entries = json.loads((out / "catalog.json").read_text())["packs"]
            self.assertGreater(len(entries), 0)
            with zipfile.ZipFile(out / "downloads/dailytools-all.zip") as all_packs:
                for item in entries:
                    name = item["id"] + "-" + item["version"] + ".zip"
                    p = out / "downloads" / name
                    self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), p.with_suffix(".zip.sha256").read_text().split()[0])
                    with zipfile.ZipFile(p) as z:
                        self.assertIn(item["id"] + "/INSTRUCTIONS.md", z.namelist())
                    self.assertIn(item["path"] + "/INSTRUCTIONS.md", all_packs.namelist())
            bundle = out / "downloads/dailytools-all.zip"
            self.assertEqual(hashlib.sha256(bundle.read_bytes()).hexdigest(), bundle.with_suffix(".zip.sha256").read_text().split()[0])
