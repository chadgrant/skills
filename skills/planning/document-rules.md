# Document rules

Use the relevant sections for the documents being changed. Check only applicable rows; a missing optional document is not itself a gap.

## Diagrams

A diagram is a teaching aid. If a reader can't grasp it in ten seconds, split it.

- **≤ 6 boxes.** A seventh box is a new diagram.
- **Split by C4 level**: Context (the system and who touches it) → Container (apps, services, stores) → Component (inside one container). Each level is its own diagram.
- **ELI5 caption** under every diagram: "In plain terms: …".
- **Spine-ID labels** on every box (`ENT-001 User`; a component tagged with its `REQ-`/`ADR-`). Labels are the sync mechanism, since scenes don't diff cleanly.
- **Excalidraw**: scenes in `docs/requirements/diagrams/`, cloned from `templates/diagram.excalidraw`. Export with "Embed scene" on to `<name>.excalidraw.svg` and embed it (`![context](diagrams/context.excalidraw.svg)`). The SVG is both picture and source; never hand-edit its paths. [StarVector](https://github.com/joanrod/star-vector) may vectorize a whiteboard photo into a starter scene, nothing more.
- Which diagram goes in which doc: `reference.md`.

## The spine

One shared ID namespace links every doc and turns "keep them in sync" into a check.

| Prefix | Lives in | Meaning |
|---|---|---|
| `REQ-###` | PRD | Functional requirement |
| `NFR-###` | PRD | Non-functional requirement (perf, security, a11y, compliance) |
| `ADR-###` | ERD | An architecture decision (one each; a changed decision supersedes the old one, which compaction then folds away) |
| `ENT-###` | DRD | A data entity / table |
| `NAV-###` | User flows | An IA / navigation node |
| `FLOW-###` | User flows | A user flow (cites the `REQ`s it stitches) |
| `SCR-###` | Wireframes | A screen (cites a `REQ`, appears in a `FLOW`) |
| `CMP-###` | Style guide | A design-system component |
| `TOK-###` | Style guide | A design token |
| `REL-###` | Release plan | A rollout step or gate |
| `SLO-###` | Observability | A service-level objective (cites the `NFR` it protects) |
| `CON-###` | Plan | A code contract: an interface, abstract class, protocol, or shared type, with its file path and doc-comment spec |
| `TASK-###` | Plan | Implements a cohesive group of `CON`s, built by one worker |
| `TEST-###` | Plan | A task's verify step; cites the `REQ` it proves |

Extension IDs, only when their doc exists: `API-###` in the API contract (each cites the `REQ` it serves and the `ENT` it touches) · `TC-###` in the Test & QA plan (scenario test cases; each cites a `REQ`/`NFR`).

**Linking rules:** every `TASK` cites the `REQ`/`NFR` it satisfies and the `CON`s it implements; every `CON` is implemented by exactly one `TASK`; every `REQ` has ≥1 `TASK` and a `TEST-`; `ENT`s trace to the `REQ`s that need them; `ADR`s are cited by the tasks that implement them; PII `ENT`s carry a classification and a retention rule; every user-facing `REQ` has ≥1 `SCR`; every `SCR` traces to a `REQ` and appears in a `FLOW`; every `SLO`/alert cites the `NFR` it protects; every irreversible `REL` step has a rollback or an explicit forward-fix-only note.

**ID scope:** unique within its prefix across the whole doc set (one continuous `TASK-` sequence across all phases).

## Traceability checklist

- [ ] Every `REQ`/`NFR` maps to ≥1 `TASK` (unmapped = unbuilt promise).
- [ ] Every `TASK` cites ≥1 `REQ`/`NFR` (uncited = scope creep or dead work).
- [ ] Every `REQ` has a `TEST-` / acceptance criterion.
- [ ] Done is defined as green **and** clean (a code-quality gate, not tests alone).
- [ ] The plan names the fast gate, the full gate (coverage with its 90% threshold, backing services, e2e), and an e2e driver that fits each surface (Playwright only for browser UI); every user-facing `REQ` has an e2e `TC-`.
- [ ] Every `ENT` traces to a `REQ`; every persisted field has a classification and each entity a retention rule.
- [ ] ERD interfaces ↔ DRD schema ↔ DRD data dictionary agree (names, types, cardinality).
- [ ] Every `ADR` is referenced by the tasks that implement it; no code contradicts an accepted `ADR`.
- [ ] Every diagram has ≤6 boxes and an ELI5 caption; bigger is split by C4 level.
- [ ] Every `ENT`/major component is an ID-labeled box, and every box maps to a spine ID.
- [ ] Every user-facing `REQ` has ≥1 `SCR`; every `SCR` traces to a `REQ` and appears in ≥1 `FLOW`; every `FLOW` cites its `REQ`s.
- [ ] Every interactive `SCR` covers empty / error / loading states; every `CMP` a screen uses exists in the style guide or is flagged net-new.
- [ ] Every `SLO`/alert cites its `NFR`; every irreversible `REL` step has a rollback or an explicit forward-fix-only note.
- [ ] No placeholders (`TBD`, "similar to above", "add error handling") in any doc.
