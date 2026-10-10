---
doc: release-plan
title: <Feature / Project name>
status: draft            # draft | in-review | approved
owner: <name>
last_synced: <date>
confluence_page_id: null # set by the Confluence connector
jira_project_key: null   # set by the Jira connector
---

# Release plan — <Feature / Project name>

> **Release, migration & rollout** · **Related:** [ERD](./erd.md) · [DRD](./drd.md) · [Observability](./observability.md) · [Plan](../plans/<file>.md)

## 1. Deployment architecture
<Where it runs and how it ships — environments, infra, the deploy path. The ERD owns the *logical* architecture; this owns the *runtime/deployment* view.>

**Deployment diagram** (environments/services/stores, ≤6 boxes; clone `templates/diagram.excalidraw`):
![deployment](diagrams/deployment.excalidraw.svg)
> *In plain terms: <where the code lives once shipped, and how a change reaches users>.*

## 2. Rollout steps
<The ordered runbook. Each `REL-` is a step or gate; feature-flag flips, staged/canary %, and cutover gates go here.>

| ID | Step | Gate / trigger | Owner |
|---|---|---|---|
| REL-001 | <e.g. deploy behind flag `X` off> | <what makes it safe to proceed> | <name> |

## 3. Data migration & backfill
<Schema-change strategy, backfill jobs, ordering vs. the deploy. Reference the DRD's migration section; don't restate the schema.>

## 4. Rollback
<Per irreversible step in §2/§3: how to reverse it, or why it can't be reversed and what the forward-fix is. Every irreversible step must have a rollback or an explicit "no rollback — forward-fix only" note.>

| Step | Reversible? | Rollback / forward-fix |
|---|---|---|
| REL-… | yes / no | <exact procedure> |

## 5. Comms & readiness
<Who is notified and when; support/on-call handoff; the go / no-go checklist that gates the release.>
