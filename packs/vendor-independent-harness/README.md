# Vendor-independent harness · v1.0.0

Portable engineering contract for Claude Code, Cursor, Codex and Antigravity.

**[Full installation and usage instructions](INSTRUCTIONS.md)** · [Daily prompts](prompts.md)

## Quick start
Requires Python 3.9+ and an existing project. Download or clone this repository and enter this pack directory.

```bash
python3 install.py /absolute/path/to/project
python3 install.py /absolute/path/to/project --apply
```
Configure `.harness/project.json` in your project and run `python3 .harness/verify.py` from its root. See INSTRUCTIONS.md for tool-specific setup, CI integration, troubleshooting and removal.

## Contents
- Shared engineering contract and tool adapters
- Architecture, task and evidence templates
- Non-overwriting installer and fail-closed verification runner
- Standalone ZIP generator (`python3 pack.py`)
- Daily engineering prompts

Instructions are advisory; configure tool permissions and CI independently.
