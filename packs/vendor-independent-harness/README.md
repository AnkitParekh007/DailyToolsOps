# Vendor-independent harness · v1.0.0

A portable engineering contract for Claude Code, Cursor, Codex and Antigravity. Requires Python 3.9+ and Git for normal use. No API keys or dependencies.

## Get started
From a terminal:
```sh
git clone https://github.com/AnkitParekh007/daily-tools-resources.git
cd daily-tools-resources/packs/vendor-independent-harness
python3 install.py /absolute/path/to/project
python3 install.py /absolute/path/to/project --apply
```
The first command previews changes. The second copies only missing files; any conflicting file aborts before writing. Review and merge conflicting instructions manually. Never overwrite existing project policies.

## Configure
1. Edit target .harness/project.json with actual lint, typecheck, test, build and security commands (argument arrays, no shell).
2. Fill in architecture.md and task.md under .harness.
3. Run from target: `python3 .harness/verify.py`. Unconfigured or failed checks fail the gate.
4. Start your coding tool and ask it to read AGENTS.md and .harness/contract.md, then execute the task template.
5. Add the verification command to your existing CI and require its status on protected branches. This pack does not modify branch protection or enable deployments.

## Tool adapters
Claude Code: CLAUDE.md imports AGENTS.md. Cursor: .cursor/rules/harness.mdc. Codex: AGENTS.md. Antigravity: .agent/rules/harness.md is a starter workspace rule; confirm the active rule location in your installed version and explicitly reference AGENTS.md if needed. Instructions are advisory, not security boundaries. Configure each tool's sandbox and approval settings separately.

## Download only this pack
Use sparse checkout:
```sh
git clone --filter=blob:none --sparse https://github.com/AnkitParekh007/daily-tools-resources.git
cd daily-tools-resources
git sparse-checkout set packs/vendor-independent-harness
```
Or download the repository ZIP from the root README and extract this folder. Create a standalone ZIP using `python3 pack.py`; it writes vendor-independent-harness-1.0.0.zip beside this README.

## Update / remove
Run preview again on a clean Git branch. Manually merge differences; no automatic upgrades or deletion. To remove, inspect your installation commit and revert only the pack-owned changes, preserving project-specific edits. Do not remove pre-existing rules.

## Daily workflow
Use prompts.md for implementation, audit, bug fix and release review. Record actual commands, exit codes and outstanding risks in evidence.md. Never infer success from an agent's summary.
