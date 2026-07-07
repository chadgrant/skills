# Roadmap

What exists in this skill today, and what's designed-for but not yet built.

## Built now
- **Adaptive doc family** — PRD, ERD, DRD, API contract, Test & QA plan, implementation plan; produced only when the project warrants each.
- **The spine** — shared ID namespace (`REQ- / NFR- / ADR- / ENT- / TASK- / TEST-`, extensions `API- / TC-`) with a hand-run traceability checklist.
- **Diagrams** — Excalidraw, ≤6 boxes, C4 split-by-zoom, ELI5 captions, ID-labeled boxes.
- **Two entry paths** — author, and re-sync (reconcile docs against current code).
- **Model routing** — per-task tiers handed to `multi-model-implementation`.
- **Connector-ready** — machine-readable front-matter on every doc + the mapping contract in `connectors.md`.

## Next (designed, not built)
- **Confluence connector** — push/pull the doc set as a page tree, upsert by `confluence_page_id`, upload diagrams as attachments.
- **Jira connector** — shred the traceability graph into an epic → stories → sub-tasks tree, upsert by spine ID, mirror tier/`observe` as labels.
- **Bidirectional status sync** — reflect Jira issue status back into doc front-matter (`status`, `last_synced`).

## Later
- **CI drift check** — run the traceability checklist automatically on PRs; fail on orphan requirements or untraceable tasks.
- **Round-trip** — accept edits made in the KB (Confluence/Jira) back into the repo docs without clobbering.

## Explicitly out of scope (for now)
- StarVector as a diagram source (optional sketch-vectorizing side-path only).
- Threat model / ops-readiness / RFC as first-class templates (add by hand when the work needs them; see the note in `SKILL.md`).
