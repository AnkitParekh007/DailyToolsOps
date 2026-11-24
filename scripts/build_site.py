"""Build static GitHub Pages site and verified downloadable archives."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import dailytools

def build(out):
    out = Path(out).resolve()
    if out.exists():
        raise ValueError("Output must not exist; choose a fresh build directory")
    if out == ROOT or out in ROOT.parents:
        raise ValueError("Unsafe output")
    entries = dailytools.catalog()
    shutil.copytree(ROOT / "website", out)
    (out / ".nojekyll").touch()
    (out / "catalog.json").write_text(json.dumps({"schema_version": 1, "packs": list(entries.values())}, indent=2), encoding="utf-8")
    downloads = out / "downloads"
    for item in entries.values():
        dailytools.archive(item, downloads)
    bundle = downloads / "dailytools-all.zip"
    with zipfile.ZipFile(bundle, "x", compression=zipfile.ZIP_DEFLATED) as z:
        for item in entries.values():
            folder = ROOT / item["path"]
            for path in sorted(folder.rglob("*")):
                if path.is_symlink():
                    raise ValueError("Symlink in pack")
                if path.is_file() and path.suffix not in (".zip", ".pyc") and "__pycache__" not in path.parts:
                    info = zipfile.ZipInfo(item["path"] + "/" + path.relative_to(folder).as_posix())
                    info.compress_type = zipfile.ZIP_DEFLATED
                    z.writestr(info, path.read_bytes())
        for rel in ("README.md", "catalog.json", "dailytools.py"):
            z.write(ROOT / rel, rel)
    bundle.with_suffix(".zip.sha256").write_text(hashlib.sha256(bundle.read_bytes()).hexdigest() + "  " + bundle.name + "\n", encoding="utf-8")
    print("Built", len(entries), "packs at", out)

if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "_site")
