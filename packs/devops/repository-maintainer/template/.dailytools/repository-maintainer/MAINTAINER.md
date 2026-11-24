# Scheduled audit and controlled remediation playbook

## Scope and evidence
Project / commit:
Owner:
Objective:
Non-goals:

## Working record
Define 15-day audit cadence, scope, issue fingerprint, severity, allowed changes, protected paths, CI gates and merge policy.

| Item | Evidence / source | Decision or status |
| --- | --- | --- |
| | | |

## Workflow
Audit read-only first; deduplicate issues; use isolated PRs; merge only after required checks and allowed policy. This pack does not enable a scheduler or autonomous execution.

## Worked example
Example: dependency vulnerability produces an issue and narrowly scoped upgrade PR; never disable failing tests.

## Agent task
Read this artifact and existing repository rules. Inspect evidence before acting. Do not invent results, bypass permissions, merge or deploy without applicable authorization.

## Acceptance checklist
- [ ] Scope and source evidence recorded
- [ ] Workflow completed or blockers documented
- [ ] Relevant tests or checks recorded with actual results
- [ ] Risks, rollback and outstanding decisions recorded
