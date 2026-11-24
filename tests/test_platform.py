import hashlib
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = "vendor-independent-harness"

class PlatformTests(unittest.TestCase):
    def cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(ROOT / "dailytools.py"), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def test_catalog(self):
        self.cli("validate")
        self.assertIn(PACK, self.cli("list"))
        self.assertIn(PACK, self.cli("search", "engineering"))
        self.cli("info", "missing", expected=1)

    def test_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.cli("install", PACK, "--target", target)
            self.assertFalse((target / "AGENTS.md").exists())
            self.cli("install", PACK, "--target", target, "--apply")
            self.assertTrue((target / ".harness/verify.py").is_file())
            self.cli("install", PACK, "--target", target, "--apply")
            (target / "AGENTS.md").write_text("existing")
            self.cli("install", PACK, "--target", target, "--apply", expected=1)
            self.assertEqual((target / "AGENTS.md").read_text(), "existing")
            run = subprocess.run([sys.executable, str(target / ".harness/verify.py")], capture_output=True)
            self.assertNotEqual(run.returncode, 0)

    def test_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.cli("download", PACK, "--output", tmp)
            path = Path(tmp) / (PACK + "-1.0.0.zip")
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), path.with_suffix(".zip.sha256").read_text().split()[0])
            with zipfile.ZipFile(path) as z:
                self.assertIn(PACK + "/INSTRUCTIONS.md", z.namelist())
                self.assertIn(PACK + "/template/.cursor/rules/harness.mdc", z.namelist())
            self.cli("download", PACK, "--output", tmp, expected=1)

if __name__ == "__main__":
    unittest.main()
