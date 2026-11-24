# Vendor-independent harness — Instructions

## 1. Prerequisites
Python 3.9+, Git and an existing project directory. No extra Python packages or API keys required. Start on a clean feature branch and back up existing changes.

## 2. Download
Download the [repository ZIP](https://github.com/AnkitParekh007/daily-tools-resources/archive/refs/heads/main.zip) and extract this pack, or use:
```bash
git clone --filter=blob:none --sparse https://github.com/AnkitParekh007/daily-tools-resources.git
cd daily-tools-resources
git sparse-checkout set packs/vendor-independent-harness
cd packs/vendor-independent-harness
```
Run `python3 pack.py` to generate a standalone ZIP.

## 3. Install
From the pack directory:
```bash
python3 install.py /absolute/path/to/project
python3 install.py /absolute/path/to/project --apply
```
Replace the path with your project location. First command previews changes; second installs missing files. Conflicting files abort preflight; merge instructions manually rather than deleting existing rules. Inspect Git status afterward; unexpected I/O errors can leave a partial installation.

## 4. Configure
Fill in .harness/architecture.md and .harness/task.md in the target. Configure .harness/project.json with actual commands. Example for an npm project with matching scripts:
```json
{
  "checks": {
    "lint": ["npm", "run", "lint"],
    "typecheck": ["npm", "run", "typecheck"],
    "test": ["npm", "test"],
    "build": ["npm", "run", "build"],
    "security": ["npm", "audit", "--audit-level=high"]
  }
}
```
For other stacks use actual equivalent commands. Review them before execution; never substitute dummy success commands.

## 5. Tool-specific usage
| Tool | Steps |
| --- | --- |
| Claude Code | Open target directory in terminal; launch Claude Code; confirm CLAUDE.md imports AGENTS.md. |
| Cursor | Open target workspace; check .cursor/rules/harness.mdc is active; start Agent. |
| Codex | Open target with CLI or IDE; ensure AGENTS.md is in scope. Commit harness files before cloud tasks. |
| Antigravity | Open target workspace; confirm active rule settings. .agent/rules/harness.md is a starter adapter; explicitly reference AGENTS.md if not discovered. |

Universal starter prompt:
> Read AGENTS.md and .harness/contract.md. Inspect architecture and task brief in .harness. Implement only the agreed scope, run configured verification, record actual evidence and stop before merge or deployment.

Configure tool permissions, sandbox and approvals independently. Instructions alone are not a security boundary.

## 6. Daily workflow
1. Create task branch or worktree.
2. Fill in task objective, non-goals, acceptance criteria and rollback in .harness/task.md.
3. Select a prompt from [prompts.md](prompts.md).
4. Review the plan and diff.
5. Run verification from the target root:
```bash
python3 .harness/verify.py
```
6. Record command results and blockers in .harness/evidence.md.
7. Obtain independent review for risky changes; merge or release only after approval.

## 7. CI integration
Add the verification command to existing CI after installing Python and project dependencies. Require the resulting check in branch protection. The pack does not configure CI or branch protection automatically.

## 8. Troubleshooting
| Symptom | Action |
| --- | --- |
| Python not found | Install Python 3.9+ or use the correct executable. |
| Installer conflict | Compare files and merge manually. |
| Configure check error | Set all five checks to nonempty executable argument arrays. |
| Command missing or timeout | Install dependencies or correct the command. |
| Agent ignores instructions | Explicitly reference the contract and confirm workspace scope. |
| Verification fails | Investigate; never bypass or misreport checks. |

## 9. Update or uninstall
Download desired version and preview on a clean branch. Merge changes manually; installer does not overwrite. To uninstall, inspect installation commit and revert only pack-owned changes, preserving later edits and pre-existing files.

## 10. Completion checklist
- [ ] Instructions loaded
- [ ] Real verification commands configured
- [ ] Acceptance criteria recorded
- [ ] Verification passed with evidence
- [ ] Diff reviewed and release approval obtained if needed
