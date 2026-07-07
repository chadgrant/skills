# Connectors — mapping guide (design, not yet built)

How the doc set maps outward to a Confluence-style knowledge base and to Jira. **No live integration ships in this skill** — this is the contract a future connector implements. The docs are already shaped for it: stable spine IDs + the YAML front-matter on every doc are all a connector needs.

## The sync contract

1. **IDs are stable and unique.** A connector **upserts by ID** — it never creates a second page/issue for an existing `REQ-`/`TASK-`. Renaming text is fine; the ID is the identity.
2. **Front-matter carries the external handles.** `confluence_page_id` and `jira_project_key` start `null`; the connector fills them on first push and reads them on every sync after.
3. **`last_synced` guards drift.** If the doc changed after `last_synced`, push; if the remote changed after it, pull or flag a conflict. Same discipline as the re-sync path, just across the boundary.
4. **Diagrams travel as attachments.** Each `*.excalidraw.svg` is uploaded as a page attachment and referenced inline; the `.excalidraw` source rides along so it stays editable.

## Confluence mapping

| Local | Confluence |
|---|---|
| The feature (doc set) | One **parent page**, titled from the PRD `title` |
| `prd.md` / `erd.md` / `drd.md` / `api-contract.md` / `test-qa-plan.md` | **Child pages** under the parent |
| `implementation-plan.md` | Child page (or left in-repo and linked, if plans stay engineering-only) |
| `*.excalidraw.svg` | Page **attachments**, embedded via the image macro |
| `confluence_page_id` (front-matter) | The stored page id used to update-in-place |

## Jira mapping

| Spine ID | Jira |
|---|---|
| PRD (the feature) | **Epic** |
| `REQ-###` / `NFR-###` | **Story** under the epic (summary = requirement, description links back to the PRD anchor) |
| `TASK-###` | **Sub-task** of the story whose `REQ` the task cites (carries file paths + verify step) |
| `TEST-###` / `TC-###` | The story's **acceptance criteria** |
| `ADR-###` | Linked Confluence page (or a "decision" issue), referenced from the stories it affects |
| difficulty / model tier | A label (`tier:top`, `observe`) so the board mirrors the routing |

**Shredding rule:** the epic→story→sub-task tree is generated from the traceability graph, so every Jira issue traces to a requirement and back — the same guarantee the [traceability checklist](SKILL.md#traceability-checklist) enforces locally. A requirement with no story, or a story with no requirement, is the same bug on either side of the boundary.

## What a connector must NOT do

- Don't sync a doc whose traceability checklist fails — push the fix first, or you replicate drift into the KB.
- Don't duplicate on rename — always resolve by ID, not by title.
- Don't flatten diagrams to images only — keep the embedded-scene SVG so they stay editable upstream.
