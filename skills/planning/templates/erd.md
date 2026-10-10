---
doc: erd
title: <Feature / Project name>
status: draft            # draft | in-review | approved
owner: <name>
last_synced: <date>
confluence_page_id: null # set by the Confluence connector
jira_project_key: null   # set by the Jira connector
---

# ERD — <Feature / Project name>

> **Engineering Requirements Document** (how we build it) · **Related:** [PRD](./prd.md) · [DRD](./drd.md) · [API](./api-contract.md) · [Plan](../plans/<file>.md)

## 1. Context & scope
<The existing landscape and what we're building into it. Satisfies: REQ-…>

## 2. Goals & non-goals
- **Goals:** <what the design must achieve.>
- **Non-goals:** <explicitly out of scope — prevents creep.>

## 3. The design
<Components, responsibilities, and how they interact. Link to code/interfaces — don't paste signatures that will rot.>

**C4 diagrams** (each ≤6 boxes; drill down a level instead of adding boxes; clone `templates/diagram.excalidraw`):

*L1 — Context* (the system + who/what touches it):
![context](diagrams/context.excalidraw.svg)
> *In plain terms: <who uses this and what it talks to>.*

*L2 — Container* (the apps/services/stores inside it):
![container](diagrams/container.excalidraw.svg)
> *In plain terms: <the moving parts and how they connect>.*

*L3 — Component* (inside one container — add only for the container that needs it):
![component](diagrams/component.excalidraw.svg)
> *In plain terms: <what's inside the key service>.*

**Interfaces & patterns:** <key APIs, the patterns to follow, boundaries. Reference DRD entities by ID (ENT-…).>

**Key trade-offs:** <the choices that matter and their consequences.>

## 4. Alternatives considered
| Option | Pros | Cons | Verdict |
|---|---|---|---|
| <A (chosen)> | | | Chosen |
| <B> | | | Rejected — <why> |

## 5. Cross-cutting concerns
- **Security / privacy:** <authN/authZ, data handling; ref NFR-…, DRD classification.>
- **Observability:** <logs, metrics, traces.>
- **Cost:** <resource / spend implications.>
- **Failure modes:** <per component: fail-open vs fail-closed.>

## 6. Decisions (ADRs)
> One decision per ADR. Never edit an accepted ADR — add a new one that supersedes it and link both.

### ADR-001: <Title>
- **Status:** Proposed | Accepted | Superseded by ADR-###
- **Context:** <forces at play.>
- **Decision:** <what we chose.>
- **Consequences:** <resulting trade-offs, good and bad.>
- **Implemented by:** TASK-… <tasks that carry out this decision.>
