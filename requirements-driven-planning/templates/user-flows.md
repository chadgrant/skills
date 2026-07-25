---
doc: user-flows
title: <Feature / Project name>
status: draft            # draft | in-review | approved
owner: <name>
last_synced: <date>
confluence_page_id: null # set by the Confluence connector
jira_project_key: null   # set by the Jira connector
---

# User flows — <Feature / Project name>

> **User flows & information architecture** · **Related:** [PRD](./prd.md) · [Wireframes](./wireframes.md) · [Style guide](../../design-system/style-guide.md)

## 1. Information architecture
<The map: where things live and how a user moves between them. Derive the screens from the PRD's `REQ-`; the flows in §2 are paths across this map.>

**Sitemap / navigation** (≤6 top-level nodes per view — split by section if more; clone `templates/diagram.excalidraw`; label each box with its `NAV-` id):
![sitemap](diagrams/sitemap.excalidraw.svg)
> *In plain terms: <what the main areas are and how you get between them, no jargon>.*

| ID | Node | Parent | URL / route | Nav label |
|---|---|---|---|---|
| NAV-001 | <screen/section name> | NAV-… / root | `/path` | <menu label> |

*(Nav nodes are the IA skeleton — traced by being ID-labeled boxes in the sitemap and by the `SCR-`/`FLOW-` that hang off them, not by a direct `REQ` cite.)*

## 2. User flows
<One flow per task the feature enables. Each flow is a path across the IA (§1) toward a `REQ-`. One diagram per flow — a branch that forks the journey becomes its own flow, not more boxes.>

### FLOW-001: <task the user is trying to do>
- **Satisfies:** REQ-…  ·  **Entry point(s):** <where the user starts — NAV-… / external link / notification>
- **Screens traversed:** SCR-… → SCR-… → SCR-…  *(each is wireframed in [wireframes.md](./wireframes.md))*

**Flow diagram** (happy path, ≤6 steps; clone `templates/diagram.excalidraw`):
![flow: <name>](diagrams/flow-<name>.excalidraw.svg)
> *In plain terms: <what the user does, start to finish, in one jargon-free sentence>.*

- **Happy path:** <step → step → success state.>
- **Branches:** <decision points and where each leads.>
- **Error / empty exits:** <what happens on failure, no-data, permission-denied, or offline — ties to the PRD's edge cases & states.>

> Repeat per flow. Keep each diagram to one journey; fork a branch into its own `FLOW-`.
