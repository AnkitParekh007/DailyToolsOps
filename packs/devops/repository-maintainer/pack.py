from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root = Path(__file__).resolve().parent
out = root / ("repository-maintainer-" + (root / "VERSION").read_text().strip() + ".zip")
with ZipFile(out, "w", ZIP_DEFLATED) as z:
    for p in sorted(root.rglob("*")):
        if p.is_file() and not p.is_symlink() and p.suffix not in (".zip", ".pyc") and "__pycache__" not in p.parts:
            z.write(p, Path("repository-maintainer") / p.relative_to(root))
print(out)
