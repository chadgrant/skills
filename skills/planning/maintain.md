# Maintain requirements

Use only the selected mode below. Load the affected documents and the applicable [document rules](document-rules.md).

## Path B: re-sync

Code is ground truth for what *is*; the PRD for what was *promised*. The same path serves drifted docs and a brownfield repo with none.

1. **Read** existing docs and the code: schema/migrations, routes, module graph, IaC/CI, dashboards/alerts, and tests (the richest signal of intent).
2. **Reconstruct or reconcile** with spine IDs, from the highest-signal source: schema→`ENT`, routes/OpenAPI→`API`, module graph/IaC→ERD C4, deploy config→release plan, alert rules→`SLO`, routes+components→sitemap/flows, tests+guards+validation→candidate `REQ`/`NFR`.
3. **Mark what code can't say.** `[extracted]` (read directly from code) · `[inferred]` (a guess from code; confirm it) · `⚠ [needs-confirmation]` (unknowable from code: retention, success metrics, PII sensitivity, ADR alternatives, SLO targets, UX intent). Never fabricate intent; leave `⚠` inline and fill it via Path C later.
4. **Report drift before editing**: orphan requirements, untraceable code, schema ↔ data-dictionary mismatches, missing PII/retention, `ADR`s the code contradicts, every `⚠`.
5. **Reconcile.** Update docs where the code is right; open tasks where it's wrong. Never silently rewrite a promise.

## Path C: focused loop

Name a doc and drive it one unit at a time ("let's do the wireframes", "add a wireframe for checkout").

1. **Locate** the doc; scaffold it from its template if missing.
2. **Load upstream**: wireframes ← user flows (`FLOW-`) ← PRD (`REQ-`); release plan ← ERD + DRD; observability ← PRD (`NFR-`) + ERD. Missing prerequisite → offer to sketch it or proceed from `REQ-`; never hard-block.
3. **Pick one unit** (a screen, a flow, an SLO) from the upstream candidates or the user's ask.
4. **Clarify** until that unit is complete, then draft it (Excalidraw scene + section).
5. **Refine** with the user until approved.
6. **Loop** to the next unit until the user says done.
7. **Write** in place: a new item takes the next spine ID; a changed item is edited where it stands, keeping its ID, with one line added to `Recent changes` (see [compact.md](compact.md)). Never regenerate the doc. Add diagram files; bump `last_synced`.
8. **Scoped check**: only the [checklist rows](document-rules.md#traceability-checklist) touching the changed IDs.

Loop discipline: one question at a time, multiple-choice when possible. After approval go straight to the next unit; don't ask "should I continue?". A unit with missing required states (a screen without empty/error states) is not done. No placeholders. Stop only when genuinely ambiguous or the user says done; a missing prerequisite is an offer (step 2), not a stop. An unknown becomes a question or a `⚠`, never an invented value.
