# Least-privilege CI/CD design

## Scope and evidence
Project / commit:
Owner:
Objective:
Non-goals:

## Working record
Define triggers, permissions, build inputs, tests, artifacts, deployment gates, secrets and rollback.

| Item | Evidence / source | Decision or status |
| --- | --- | --- |
| | | |

## Workflow
Separate untrusted PR checks from privileged release jobs; pin dependencies; verify artifacts before deployment.

## Worked example
Example: PR runs read-only tests; production deployment uses protected environment.

## Agent task
Read this artifact and existing repository rules. Inspect evidence before acting. Do not invent results, bypass permissions, merge or deploy without applicable authorization.

## Acceptance checklist
- [ ] Scope and source evidence recorded
- [ ] Workflow completed or blockers documented
- [ ] Relevant tests or checks recorded with actual results
- [ ] Risks, rollback and outstanding decisions recorded
