# DailyToolsOps roadmap

Status as of 2026-11-24: 35 registered packs (23 core, 12 framework guides), mostly guided templates. The platform, catalog, CLI preview/install and ZIP generation are merged. The documentation portal PR #8 is not yet validated. Website deployment and individual public links require verification. No claim of full autonomous execution.

## R1 — Reliability and distribution (P0)
- [ ] [#9](https://github.com/AnkitParekh007/DailyToolsOps/issues/9) Fix docs CI and verify deployment.
- [ ] [#10](https://github.com/AnkitParekh007/DailyToolsOps/issues/10) Ownership ledger, safe upgrade and uninstall.
- [ ] [#11](https://github.com/AnkitParekh007/DailyToolsOps/issues/11) Immutable release ZIPs and checksums.

## R2 — Executable AI foundations (P0/P1)
- [ ] [#12](https://github.com/AnkitParekh007/DailyToolsOps/issues/12) Agent starter: offline reference implementation.
- [ ] [#13](https://github.com/AnkitParekh007/DailyToolsOps/issues/13) Evaluation and guardrail utilities.
- [ ] [#15](https://github.com/AnkitParekh007/DailyToolsOps/issues/15) Agent skills, prompt engineering, structured output.
- [ ] [#16](https://github.com/AnkitParekh007/DailyToolsOps/issues/16) Multi-agent orchestration; runnable RAG/MCP examples.
- [ ] [#24](https://github.com/AnkitParekh007/DailyToolsOps/issues/24) Observability, cost and reliability utilities.

## R3 — Daily software engineering (P1)
- [ ] [#14](https://github.com/AnkitParekh007/DailyToolsOps/issues/14) Architecture, feature development, refactoring.
- [ ] [#17](https://github.com/AnkitParekh007/DailyToolsOps/issues/17) Test engineering, API testing, visual regression.
- [ ] [#18](https://github.com/AnkitParekh007/DailyToolsOps/issues/18) Design systems, accessibility, performance.
- [ ] [#19](https://github.com/AnkitParekh007/DailyToolsOps/issues/19) Dependency security, data privacy, engineering evidence.
- [ ] [#20](https://github.com/AnkitParekh007/DailyToolsOps/issues/20) API, database, container engineering.

## R4 — Delivery and productivity (P1/P2)
- [ ] [#21](https://github.com/AnkitParekh007/DailyToolsOps/issues/21) Repository maintainer executable audit and PR engineering.
- [ ] [#22](https://github.com/AnkitParekh007/DailyToolsOps/issues/22) Six role-based bundles: AI architect, full-stack, frontend, production, open-source maintainer, FDE.
- [ ] [#23](https://github.com/AnkitParekh007/DailyToolsOps/issues/23) macOS developer utilities, Git productivity, secret management.

## R5 — Remaining catalog and community (P2)
- [ ] [#25](https://github.com/AnkitParekh007/DailyToolsOps/issues/25) Technical debt management, model router, human-in-the-loop, AI red teaming (defensive), local AI, legacy modernization, browser automation, performance testing, chaos engineering, open-source launch, infrastructure engineering, cloud deployment, incident response, developer environment, developer knowledge base, technical research, AI coding benchmark, project bootstrap, engineering estimation, learning and knowledge extraction, open-source marketing.
- [ ] [#26](https://github.com/AnkitParekh007/DailyToolsOps/issues/26) Contributor documentation, issue templates, roadmap discovery.

## Target
Expand from 35 to 80 registered packs: 68 core and 12 framework extensions. Existing templates must be labeled as such; runnable tools must have reproducible tests. The 45 missing core packs are covered by R2–R5. Upgrades to existing packs do not increase pack count. Target is a roadmap, not a commitment to a date.

## Definition of done
Every pack has a unique ID, manifest, VERSION, README.md, INSTRUCTIONS.md, practical artifacts, preview-first installation, individual ZIP and checksum, tests, and an automatically generated guide. Preserve user files, avoid secrets, and document verified tool compatibility. No release on failed checks. For executable tools, test failure paths and permission boundaries. Link implementation PRs to issues; close issues only when acceptance criteria are satisfied.

[Issue backlog](https://github.com/AnkitParekh007/DailyToolsOps/issues)
