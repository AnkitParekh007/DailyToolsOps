"""Local resource catalog and safe pack installer (Python 3.9+)."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
TOOLS = {"claude-code", "cursor", "codex", "antigravity"}

def catalog():
    data = json.loads((ROOT / "catalog.json").read_text())
    if data["schema_version"] != 1:
        raise ValueError("Unsupported catalog schema")
    entries = {}
    for item in data["packs"]:
        name = item["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name in entries:
            raise ValueError("Invalid or duplicate pack ID")
        if set(item) != {"id", "version", "category", "description", "tools", "path"}:
            raise ValueError("Invalid manifest fields")
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", item["version"]):
            raise ValueError("Invalid version")
        if not isinstance(item["tools"], list) or not item["tools"] or not set(item["tools"]) <= TOOLS or len(set(item["tools"])) != len(item["tools"]):
            raise ValueError("Invalid tool list")
        if not all(isinstance(item[k], str) and item[k].strip() for k in ("category", "description")):
            raise ValueError("Invalid metadata")
        rel = Path(item["path"])
        folder = ROOT / rel
        if rel.is_absolute() or ".." in rel.parts or not rel.parts or rel.parts[0] != "packs" or rel.name != name or folder.resolve() != folder:
            raise ValueError("Unsafe pack path")
        for required in ("README.md", "INSTRUCTIONS.md", "VERSION", "manifest.json", "install.py", "pack.py"):
            if not (folder / required).is_file() or (folder / required).is_symlink():
                raise ValueError("Missing or unsafe file: " + str(folder / required))
        if json.loads((folder / "manifest.json").read_text()) != item or (folder / "VERSION").read_text().strip() != item["version"]:
            raise ValueError("Manifest/version mismatch: " + name)
        entries[name] = item
    return entries

def archive(item, output):
    folder = ROOT / item["path"]
    output = output.resolve()
    if output == folder or folder in output.parents:
        raise ValueError("Output must be outside pack")
    output.mkdir(parents=True, exist_ok=True)
    dest = output / (item["id"] + "-" + item["version"] + ".zip")
    digest = dest.with_suffix(".zip.sha256")
    if dest.exists() or dest.is_symlink() or digest.exists() or digest.is_symlink():
        raise ValueError("Output already exists")
    files = []
    for path in sorted(folder.rglob("*")):
        if path.is_symlink():
            raise ValueError("Symlink in pack: " + str(path))
        if path.is_file() and path.suffix not in (".zip", ".pyc") and "__pycache__" not in path.parts:
            files.append(path)
    with zipfile.ZipFile(dest, "x", compression=zipfile.ZIP_DEFLATED) as z:
        for path in files:
            info = zipfile.ZipInfo(item["id"] + "/" + path.relative_to(folder).as_posix())
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, path.read_bytes())
    with digest.open("x") as f:
        f.write(hashlib.sha256(dest.read_bytes()).hexdigest() + "  " + dest.name + "\n")
    print(dest)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for cmd in ("list", "validate"):
        sub.add_parser(cmd)
    sub.add_parser("search").add_argument("query")
    sub.add_parser("info").add_argument("pack")
    install = sub.add_parser("install")
    install.add_argument("pack")
    install.add_argument("--target", type=Path, default=Path.cwd())
    install.add_argument("--apply", action="store_true", help="Write files; default is preview")
    download = sub.add_parser("download")
    download.add_argument("pack")
    download.add_argument("--output", type=Path, default=Path("dist"))
    args = parser.parse_args()
    try:
        entries = catalog()
        if args.command == "validate":
            print("Validated", len(entries), "pack(s)")
        elif args.command in ("list", "search"):
            for name, item in entries.items():
                if args.command == "list" or args.query.lower() in json.dumps(item).lower():
                    print(name, item["version"], "-", item["description"])
        elif args.command == "info":
            print(json.dumps(entries[args.pack], indent=2))
        elif args.command == "download":
            archive(entries[args.pack], args.output)
        else:
            item = entries[args.pack]
            cmd = [sys.executable, str(ROOT / item["path"] / "install.py"), str(args.target.resolve())]
            if args.apply:
                cmd.append("--apply")
            return subprocess.run(cmd, check=False).returncode
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
