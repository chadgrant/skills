---
doc: observability
title: <Feature / Project name>
status: draft            # draft | in-review | approved
owner: <name>
last_synced: <date>
confluence_page_id: null # set by the Confluence connector
jira_project_key: null   # set by the Jira connector
---

# Observability — <Feature / Project name>

> **SLOs, dashboards & alerts** · **Related:** [PRD](./prd.md) (NFR-) · [ERD](./erd.md) · [Release plan](./release-plan.md)

## 1. What "healthy" means
<The signals (SLIs) that show the feature is working, and the objectives (SLOs) on them. Each `SLO-` targets a PRD `NFR-` — an SLO with no `NFR` is unmoored; an `NFR` with no `SLO` is unmonitored.>

| ID | SLI (what we measure) | SLO (target) | Protects |
|---|---|---|---|
| SLO-001 | <e.g. p95 checkout latency> | <e.g. < 400ms, 99.9%> | NFR-… |

## 2. Signal flow *(optional diagram)*
<How signals get from the service to a dashboard/alert, when it aids understanding (≤6 boxes; clone `templates/diagram.excalidraw`).>
![signal flow](diagrams/signal-flow.excalidraw.svg)
> *In plain terms: <how we'd know if this broke>.*

## 3. Dashboards
<What each dashboard shows and who watches it. Link to the dashboard-as-code where it lives; don't paste screenshots that rot.>

| Dashboard | Shows | Audience |
|---|---|---|
| <name> | <the SLIs / breakdowns> | <on-call / product / …> |

## 4. Alerts
<Each alert fires on an `SLO-` breach and cites the `NFR-` it protects. State the threshold, severity, and who it pages — no alert without an owner and an action.>

| Alert | Fires when | Severity | Pages | Protects |
|---|---|---|---|---|
| <name> | SLO-… breached (<condition>) | page / ticket | <on-call> | NFR-… |

## 5. Runbook pointer
<Where the on-call runbook for these alerts lives. What to do when each fires.>
