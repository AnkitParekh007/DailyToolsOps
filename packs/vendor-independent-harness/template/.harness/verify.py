"""Fail closed unless all configured checks pass."""
import json
from pathlib import Path
import subprocess
import sys

def main():
    root = Path(__file__).resolve().parent.parent
    try:
        checks = json.loads((root / ".harness/project.json").read_text())["checks"]
        for name in ("lint", "typecheck", "test", "build", "security"):
            cmd = checks.get(name)
            if not isinstance(cmd, list) or not cmd or not all(isinstance(x, str) and x for x in cmd):
                raise ValueError("Configure check: " + name)
        failed = False
        for name, cmd in checks.items():
            if not isinstance(cmd, list) or not cmd or not all(isinstance(x, str) and x for x in cmd):
                raise ValueError("Invalid command: " + name)
            print("RUN", name, flush=True)
            try:
                code = subprocess.run(cmd, cwd=root, timeout=900, check=False).returncode
            except (OSError, subprocess.TimeoutExpired) as exc:
                print("BLOCKED", name, exc)
                failed = True
                continue
            print("RESULT", name, code, flush=True)
            failed |= code != 0
        return int(failed)
    except (OSError, ValueError, KeyError, AttributeError) as exc:
        print("BLOCKED:", exc, file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
