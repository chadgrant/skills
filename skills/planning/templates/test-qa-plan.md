---
doc: test-plan
title: <Feature / Project name> — Test & QA Plan
status: draft            # draft | in-review | approved
owner: <name>
last_synced: <date>
confluence_page_id: null # set by the Confluence connector
jira_project_key: null   # set by the Jira connector
---

# Test & QA Plan — <Feature / Project name>

> **Related:** [PRD](./prd.md) · [ERD](./erd.md) · [DRD](./drd.md) · [Plan](../plans/<file>.md)

## 1. Scope & objectives
<What this plan proves works. In-scope vs. out-of-scope test surfaces.>

## 2. Test strategy
<Levels and where each runs: unit · integration · end-to-end · manual/exploratory. Tooling, test environments, and CI stage for each.>

- **Fast gate:** `<command>`: unit tests and static checks, no services. Run by every worker.
- **Coverage** (full gate): `<command>` fails under 90% line coverage. Exclusions: <generated / vendored paths, or none>.
- **Backing services:** `<compose.test.yaml>` starts <real Postgres / queue / cache> for integration and e2e tests in the full gate, which only the orchestrator runs, once per milestone. No mocks or in-memory substitutes.
- **End-to-end:** `<command>` brings the stack up with Docker Compose and drives <browser UI → Playwright · HTTP API → requests to the running service · CLI → the built binary>. Use the driver that fits the surface; no Playwright without a browser UI.

- **Runtime recipe:** <link existing launch/doctor/drive/cleanup instructions; use the verification skill if missing>. Record the tested build, action and result evidence, owned-resource cleanup, and artifact paths that survive teardown.

## 3. Test matrix
> Each `TC-###` verifies one or more `REQ-`/`NFR-` and rolls up to a release gate. Per-task `TEST-` (in the plan) are the unit-level checks; these are the scenario-level cases above them.

| ID | Verifies | Level | Scenario | Acceptance (pass condition) |
|---|---|---|---|---|
| TC-001 | REQ-001 | e2e | <user does X end to end> | <observable pass> |

## 4. Non-functional testing
| NFR | What we test | How | Target |
|---|---|---|---|
| NFR-001 | performance / security / a11y / load | <tool / method> | <budget> |

## 5. Test data & fixtures
<Fixtures needed; how PII-safe/synthetic data is generated (ref DRD classification — never real PII in test envs).>

## 6. Entry & exit criteria
- **Entry:** <what must be true before testing starts.>
- **Exit / release gate:** <the pass bar — e.g. all Must `TC-` green, coverage ≥ 90%, e2e suite green, no open Sev-1, NFR budgets met.>

## 7. Risks & gaps
<Known untested areas and why; residual risk accepted.>
