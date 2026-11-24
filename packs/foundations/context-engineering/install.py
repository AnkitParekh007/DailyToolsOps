"""Preview or install missing harness files without overwriting."""
import argparse
from pathlib import Path
import shutil

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = args.target.resolve(strict=True)
    if not root.is_dir():
        parser.error("target must be an existing directory")
    source = Path(__file__).resolve().parent / "template"
    pending, conflicts = [], []
    for src in sorted(source.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(source)
        dst = root / rel
        if any(p.is_symlink() for p in [dst, *dst.parents] if p != root and root in p.parents):
            conflicts.append(str(rel))
        elif dst.exists():
            if not dst.is_file() or dst.read_bytes() != src.read_bytes():
                conflicts.append(str(rel))
        elif any(p.exists() and not p.is_dir() for p in dst.parents):
            conflicts.append(str(rel))
        else:
            pending.append((src, dst))
            print("ADD", rel)
    if conflicts:
        parser.exit(1, "Conflicts; nothing written: " + ", ".join(conflicts) + "\n")
    if args.apply:
        for src, dst in pending:
            dst.parent.mkdir(parents=True, exist_ok=True)
            with dst.open("xb") as out:
                out.write(src.read_bytes())
        print("Installed. Configure .harness/project.json before verification.")
    else:
        print("Preview only. Use --apply to install.")

if __name__ == "__main__":
    main()
