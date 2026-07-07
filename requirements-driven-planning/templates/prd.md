---
doc: prd
title: <Feature / Project name>
status: draft            # draft | in-review | approved
owner: <name>
last_synced: <date>
confluence_page_id: null # set by the Confluence connector
jira_project_key: null   # set by the Jira connector
---

# PRD — <Feature / Project name>

> **Related:** [ERD](./erd.md) · [DRD](./drd.md) · [API](./api-contract.md) · [Test plan](./test-qa-plan.md) · [Plan](../plans/<file>.md)

## 1. Summary
<One paragraph: what this is and its scope. Understandable in 30 seconds.>

## 2. Problem statement
<The customer pain, quantified with data. Why now.>

## 3. Goals & success metrics
| Metric | Baseline | Target | How measured |
|---|---|---|---|
| <metric> | <now> | <target> | <source> |

**Non-goals:** <what this explicitly does not do.>

## 4. Users & context
<Personas, validation, competitive/market context.>

## 5. Proposed solution
<Directional — flows, wireframes, mockups. The *what*, not the *how* (that's the ERD).>

**User flow** (≤6 steps; clone `templates/diagram.excalidraw`):
![user flow](diagrams/user-flow.excalidraw.svg)
> *In plain terms: <one jargon-free sentence — what the user does, start to finish>.*

## 6. Functional requirements
| ID | Requirement | Priority | Acceptance criterion (proven by `TEST-###` in the plan) |
|---|---|---|---|
| REQ-001 | <testable statement> | Must / Should / Could | <observable pass condition> |

## 7. Non-functional requirements
| ID | Category | Requirement / budget |
|---|---|---|
| NFR-001 | Performance / Security / A11y / Compliance | <measurable target> |

## 8. Edge cases & states
<Empty, error, permission, offline, concurrent, first-run states.>

## 9. Dependencies & risks
| Risk / dependency | Impact | Mitigation |
|---|---|---|
| <item> | <H/M/L> | <plan> |

## 10. Release criteria
<The gates that decide ship / no-ship.>
