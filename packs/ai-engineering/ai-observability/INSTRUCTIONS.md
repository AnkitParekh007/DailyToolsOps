# Privacy-conscious agent tracing — instructions

## Prerequisites
Python 3.9+, existing project directory, optional AI coding agent. Review the pack before installing.

## Download and install
From this pack directory run:
```sh
python3 install.py /absolute/path/to/project
python3 install.py /absolute/path/to/project --apply
``
Preview first; conflicts abort preflight. Run `python3 pack.py` to create the individual ZIP. From the resource repository root you can also use `python3 dailytools.py install ai-observability --target /path/to/project --apply`.

## Use
Open `.dailytools/ai-observability/TRACE.md` in your target project. Populate it with evidence and ask Claude Code, Cursor, Codex or Antigravity to read that file and follow its workflow. Respect existing project instructions. No agent configuration is silently changed.

Correlate parent/child operations; redact secrets; monitor latency, failure and cost without storing raw sensitive prompts.

## Example
Example: trace a timeout across retrieval and model stages using correlation IDs.

## Validate
Check all acceptance criteria in the artifact; run actual project tests where applicable. Installation alone is not evidence of successful engineering work.

## Troubleshoot, update and remove
On conflict compare and merge manually; on missing Python install a supported runtime. Preview newer versions; preserve existing edits. To remove, review Git diff and revert only pack-owned files. Do not delete unrelated data.
