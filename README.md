# Daily Tools & Resources

Vendor-independent engineering resources for Claude Code, Cursor, Codex and Antigravity.

| Pack | Version | Guide |
| --- | --- | --- |
| [Vendor-independent harness](packs/vendor-independent-harness/) | 1.0.0 | [Instructions](packs/vendor-independent-harness/INSTRUCTIONS.md) |

## Quick start
Requires Python 3.9+. Clone the repository, then run:
```sh
python3 dailytools.py list
python3 dailytools.py info vendor-independent-harness
python3 dailytools.py install vendor-independent-harness --target /path/to/project
python3 dailytools.py install vendor-independent-harness --target /path/to/project --apply
python3 dailytools.py download vendor-independent-harness
```
Installation previews by default. Download builds a standalone ZIP and SHA-256 file locally in dist/. CI produces downloadable workflow artifacts. No remote release assets are published automatically. Review code before running. [Repository ZIP](https://github.com/AnkitParekh007/daily-tools-resources/archive/refs/heads/main.zip).

## Contribute a pack
Provide README.md, INSTRUCTIONS.md, VERSION, manifest.json, install.py and pack.py. Register in catalog.json. Run python3 dailytools.py validate and python3 -m unittest discover -s tests -v. Never overwrite project files or include secrets. See [roadmap](docs/ROADMAP.md).
