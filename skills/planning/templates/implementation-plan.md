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
- **Coverage:** `<command>` fails under 90% line coverage. Exclusions: <paths, or none>
- **Backing services for tests:** `<compose.test.yaml>` (real database / queue / cache; no mocks)
- **End-to-end:** `<command>`, driver: <Playwright for browser UI · HTTP for an API · the built binary for a CLI · n/a for a library>

## Requirements covered
<REQ-/NFR- IDs this plan satisfies. Every one must map to ≥1 task below.>

---

## Phase GOAL-1: <milestone name>  ·  exit criterion: <what proves it done>

### TASK-001: <feature slice: what a user can now do>
- **Satisfies:** REQ-… / NFR-…  ·  **Implements:** ADR-… (if any)
- **Difficulty:** Easy | Medium | Hard  ·  **Model tier:** small | mid | top  ·  **Flags:** `observe` (if security/money/auth/data-integrity)
- **Owns:** <directories or packages; disjoint from other tasks in the same phase>
- **Interfaces — Exposes:** <signatures other tasks call; blank if none.>
- **Interfaces — Consumes:** <what earlier tasks expose that this needs.>
- **Depends on:** TASK-… (cross-phase ordering; blank if none)
- **Delivers:** <the end-to-end behavior, through every layer it touches (schema, logic, API, UI).>
- **TEST-001 (verify, no interpretation):** `<exact command>` → `<exact expected output>`  ·  proves REQ-…

> Repeat per task: usually 5–15 per project, each a few hundred to about 1,500 changed lines. Tasks in the same phase own **disjoint directories** so they can run in parallel. A phase ends in one review of the whole feature.

---

## Alternatives / dependencies / risks
- **Rejected approaches:** <ALT-…>
- **External dependencies & ordering:** <DEP-…>
- **Risks & assumptions:** <RISK-… / ASSUMPTION-…>
