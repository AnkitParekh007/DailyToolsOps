# Bounded retries and recovery

## Scope and evidence
Project / commit:
Owner:
Objective:
Non-goals:

## Working record
Define idempotency keys, retryable errors, max attempts, backoff, timeouts, checkpoints, circuit breaker and terminal state.

| Item | Evidence / source | Decision or status |
| --- | --- | --- |
| | | |

## Workflow
Retry only safe transient failures; reconcile uncertain writes before retrying; test crashes and duplicate deliveries.

## Worked example
Example: after a timed-out write, query by idempotency key before issuing another write.

## Agent task
Read this artifact and existing repository rules. Inspect evidence before acting. Do not invent results, bypass permissions, merge or deploy without applicable authorization.

## Acceptance checklist
- [ ] Scope and source evidence recorded
- [ ] Workflow completed or blockers documented
- [ ] Relevant tests or checks recorded with actual results
- [ ] Risks, rollback and outstanding decisions recorded
