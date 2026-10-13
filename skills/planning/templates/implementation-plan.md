---
doc: plan
title: <Feature name>
status: draft            # draft | ready
owner: <name>
last_synced: <date>
confluence_page_id: null # set by the Confluence connector
jira_project_key: null   # set by the Jira connector — PRD→epic, TASK-→stories
---

# <Feature name> — Implementation Plan

> **For the build:** hand this plan to the `chadgrant:implementation` skill to orchestrate the waves. Each task carries a **model tier**; the orchestrator dispatches (each worker follows the same skill's worker manual), verifies, and commits per task.
>
> **Sources:** [PRD](../requirements/prd.md) · [ERD](../requirements/erd.md) · [DRD](../requirements/drd.md) · [API](../requirements/api-contract.md) · [Test plan](../requirements/test-qa-plan.md)

**Goal:** <one sentence.>

**Architecture:** <2–3 sentences, per the ERD.>

**Tech stack:** <key technologies.>

## Global constraints
<Version floors, dependency limits, naming/copy rules, platform requirements — one line each, copied verbatim from the PRD/ERD. Every task implicitly includes these.>

- **Static gate:** `<command>` (format check, lint, type-check, complexity limit)
- **Fast gate:** `<command>` (unit tests + static gate; no Docker, no services; workers run it)
- **Full gate:** `<command>` (integration tests against `<compose.test.yaml or n/a>`, coverage failing under 90%, e2e with <Playwright for browser UI · HTTP for an API · the built binary for a CLI · n/a>; the orchestrator runs it once per milestone). Coverage exclusions: <paths, or none>
- **Hot files:** <files every feature edits, and how M0 prepares them to take additions without conflict>

## Requirements covered
<REQ-/NFR- IDs this plan satisfies. Every one must map to ≥1 task below.>

---

## Phase GOAL-1: <milestone name>  ·  exit criterion: <what proves it done>

### Contracts (written first, by one task, before any other task starts)

| ID | Kind | File | Members | Behavior the doc comment states (errors, invariants, an example) |
|---|---|---|---|---|
| CON-001 | <interface · abstract class · protocol · shared type> | `<final path>` | <signatures> | <…> |

### TASK-001: <the module or part of the feature it implements>
- **Satisfies:** REQ-… / NFR-…  ·  **Implements:** ADR-… (if any)
- **Difficulty:** Easy | Medium | Hard  ·  **Model tier:** small | mid | top  ·  **Flags:** `observe` (if security/money/auth/data-integrity)
- **Hot files:** <which of the plan's hot files this task adds to, if any>
- **Implements:** CON-… (exactly one task per contract)
- **Consumes:** CON-… (built against their stubs; no waiting)
- **Depends on:** TASK-… (only when a stub can't stand in; usually blank)
- **Delivers:** <the end-to-end behavior, through every layer it touches (schema, logic, API, UI).>
- **TEST-001 (verify, no interpretation):** `<exact command>` → `<exact expected output>`  ·  proves REQ-…

> Repeat per task: usually 5–15 per project, each a few hundred to about 1,500 changed lines. Each task runs in its own worktree against the merged contracts; tasks in a phase run in parallel and are merged by the orchestrator. A phase ends in one review of the whole feature.

---

## Alternatives / dependencies / risks
- **Rejected approaches:** <ALT-…>
- **External dependencies & ordering:** <DEP-…>
- **Risks & assumptions:** <RISK-… / ASSUMPTION-…>
