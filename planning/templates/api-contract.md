---
doc: api
title: <Feature / Project name> — API / Interface Contract
status: draft            # draft | in-review | approved
owner: <name>
last_synced: <date>
confluence_page_id: null # set by the Confluence connector
jira_project_key: null   # set by the Jira connector
---

# API / Interface Contract — <Feature / Project name>

> **Related:** [PRD](./prd.md) · [ERD](./erd.md) · [DRD](./drd.md)
> **Source of truth:** link the machine-readable spec (OpenAPI / AsyncAPI / proto) here and keep it authoritative — this doc explains it, the spec defines it.

## 1. Overview & style
<REST | GraphQL | gRPC | async/events. Base URL, media types, versioning scheme (e.g. `/v1`).>

## 2. Authentication & authorization
<Scheme (OAuth2 / API key / mTLS), scopes/roles, per NFR-… .>

## 3. Operations
> One `API-###` per operation. Each cites the `REQ-` it serves and the `ENT-` it reads/writes.

### API-001: <name> — `POST /v1/resource`
- **Serves:** REQ-…  ·  **Touches:** ENT-…
- **Request:** `<shape / link to schema>`
- **Response (200):** `<shape / link to schema>`
- **Errors:** `<status → error code → meaning>`
- **Idempotency / side effects:** `<notes>`

**Key-interaction sequence** (≤6 boxes; clone `templates/diagram.excalidraw`):
![api sequence](diagrams/api-sequence.excalidraw.svg)
> *In plain terms: <who calls what, and what comes back>.*

## 4. Schemas / models
<Request/response models. Link each field back to DRD `ENT-`/data-dictionary rather than re-defining types.>

## 5. Error model
<Uniform error envelope, status-code conventions, retryable vs. terminal.>

## 6. Compatibility & versioning
<Breaking-change policy, deprecation window, how consumers are notified.>

## 7. Rate limits & SLAs
<If public/consumed externally: quotas, throttling, availability target.>
