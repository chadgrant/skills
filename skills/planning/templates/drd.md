---
doc: drd
title: <Feature / Project name>
status: draft            # draft | in-review | approved
owner: <name>
last_synced: <date>
confluence_page_id: null # set by the Confluence connector
jira_project_key: null   # set by the Jira connector
---

# DRD — <Feature / Project name>

> **Data Requirements Document** · **Related:** [PRD](./prd.md) · [ERD](./erd.md) · [API](./api-contract.md)

## 1. Scope & owners
<Data domains/systems in scope; data owner(s). Satisfies: REQ-…>

## 2. Conceptual ER model
<Entities and relationships with cardinality. ≤6 entities per view — split by subdomain if more. Clone `templates/diagram.excalidraw`; label each box with its `ENT-` id.>
![er model](diagrams/er-model.excalidraw.svg)
> *In plain terms: <what each entity is and how they relate, no jargon>.*

## 3. Physical schema
<Tables, primary/foreign keys, indexes, constraints. Link to migrations rather than pasting full DDL where possible.>

## 4. Data dictionary
| Entity | Field | Type | Allowable values | Nullable | Description |
|---|---|---|---|---|---|
| ENT-001 User | email | text | RFC-5322 | no | login identity |

## 5. Classification & PII
| Entity.field | Sensitivity | PII? | Notes |
|---|---|---|---|
| ENT-001.email | Confidential | Yes | direct identifier |

*(Sensitivity: Public / Internal / Confidential / Restricted.)*

## 6. Lifecycle & lineage
<Where data is collected, how it flows, where it's stored — including backups and replicas.>

**Data-flow** (collect → store → delete, ≤6 boxes):
![data flow](diagrams/data-flow.excalidraw.svg)
> *In plain terms: <where this data comes from, where it lives, when it's deleted>.*

## 7. Retention & deletion
| Entity | Retention period | Purge / anonymize rule | Legal basis |
|---|---|---|---|
| ENT-001 User | <e.g. 7y after close> | <hard delete / anonymize> | <contract / GDPR / …> |

## 8. Access & security
<Who can read/write each entity; encryption at rest/in transit; masking. Ref NFR-… / ERD cross-cutting concerns.>

## 9. Migration & versioning
<Schema-change strategy, backfill plan, backward-compat window, rollback.>
