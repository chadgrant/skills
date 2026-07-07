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

> **For the build:** hand this plan to the `multi-model-implementation` (model-routed-delivery) skill to orchestrate the waves. Each task carries a **model tier**; the orchestrator dispatches, verifies, and commits per task.
>
> **Sources:** [PRD](../requirements/prd.md) · [ERD](../requirements/erd.md) · [DRD](../requirements/drd.md) · [API](../requirements/api-contract.md) · [Test plan](../requirements/test-qa-plan.md)

**Goal:** <one sentence.>

**Architecture:** <2–3 sentences, per the ERD.>

**Tech stack:** <key technologies.>

## Global constraints
<Version floors, dependency limits, naming/copy rules, platform requirements — one line each, copied verbatim from the PRD/ERD. Every task implicitly includes these.>

## Requirements covered
<REQ-/NFR- IDs this plan satisfies. Every one must map to ≥1 task below.>

---

## Phase GOAL-1: <milestone name>  ·  exit criterion: <what proves it done>

### TASK-001: <component name>
- **Satisfies:** REQ-… / NFR-…  ·  **Implements:** ADR-… (if any)
- **Difficulty:** Easy | Medium | Hard  ·  **Model tier:** small | mid | top  ·  **Flags:** `observe` (if security/money/auth/data-integrity)
- **Files:** Create `path/…` · Modify `path/…:LINES` · Test `path/…`
- **Interfaces — Produces:** <exact signatures later tasks depend on.>
- **Interfaces — Consumes:** <what earlier tasks/interfaces this needs.>
- **Depends on:** TASK-… (cross-phase ordering; blank if none)
- **Steps:**
  - [ ] Write the failing test — `<test code / name>`
  - [ ] Run it, confirm it fails — `<command>` → expected: FAIL
  - [ ] Implement — `<what, concretely>`
  - [ ] Run tests, confirm pass — `<command>` → expected: PASS
- **TEST-001 (verify, no interpretation):** `<exact command>` → `<exact expected output>`  ·  proves REQ-…

> Repeat per task. Tasks in the same phase must touch **disjoint files** so they can run in parallel.

---

## Alternatives / dependencies / risks
- **Rejected approaches:** <ALT-…>
- **External dependencies & ordering:** <DEP-…>
- **Risks & assumptions:** <RISK-… / ASSUMPTION-…>
