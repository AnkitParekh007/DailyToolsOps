import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
class PackTests(unittest.TestCase):
    def test_each_pack(self):
        for item in json.loads((ROOT / "catalog.json").read_text())["packs"]:
            with self.subTest(pack=item["id"]), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "target"
                target.mkdir()
                cmd = [sys.executable, str(ROOT / "dailytools.py"), "install", item["id"], "--target", str(target)]
                subprocess.run(cmd, check=True)
                self.assertEqual(list(target.iterdir()), [])
                subprocess.run(cmd + ["--apply"], check=True)
                self.assertTrue(list(target.rglob("*.md")))
                subprocess.run(cmd + ["--apply"], check=True)
                subprocess.run([sys.executable, str(ROOT / "dailytools.py"), "download", item["id"], "--output", tmp], check=True)
                with zipfile.ZipFile(Path(tmp) / (item["id"] + "-" + item["version"] + ".zip")) as z:
                    self.assertIn(item["id"] + "/INSTRUCTIONS.md", z.namelist())
