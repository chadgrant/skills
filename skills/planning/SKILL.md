---
name: planning
description: Create durable requirements and implementation plans, iterate a requirements document, reconcile docs with code, or compact accumulated requirements history. Use for features, projects, and migrations; not trivial fixes or throwaway spikes.
---

# Requirements-driven planning

Requirements record what was promised; code records what exists. Keep them linked by stable IDs and resolve differences explicitly. Announce the selected mode, then read only its procedure.

| Request | Mode and procedure |
|---|---|
| New work needing a requirements set and routed plan | **A · Author:** [author.md](author.md) |
| Reconcile drift, or reconstruct docs from an existing repo | **B · Re-sync:** [maintain.md](maintain.md#path-b-re-sync) |
| Draft or refine one document, screen, flow, or SLO | **C · Focused loop:** [maintain.md](maintain.md#path-c-focused-loop) |
| Fold amendments and outdated history into current requirements | **D · Compact:** [compact.md](compact.md) |

## Shared rules

- Load only the documents, templates, and reference sections needed for the selected mode. A compaction does not need authoring templates or implementation manuals.
- Ask only questions that change the outcome; find factual answers in the repo. Respect decisions and authorization already supplied. Unknowable intent becomes a question or `⚠ [needs-confirmation]`, never an invented fact.
- Keep each fact in one authoritative document and cite its spine ID elsewhere. Edit changed requirements in place, preserving IDs; Git holds history. Use [compact.md](compact.md) for retiring IDs and pruning `Recent changes`.
- Follow project paths; otherwise requirements live in `docs/requirements/`, plans in `docs/plans/`, and the reusable style guide in `design-system/`. Create the domain `GLOSSARY.md` before a new doc set.
- Use [document-rules.md](document-rules.md) for the ID namespace, diagram rules, and applicable traceability checks before handoff. Read [reference.md](reference.md) only for the doc type being authored and select its template from `templates/`.
- Final documents contain concrete decisions and acceptance criteria, no unresolved scaffolding such as `TBD` or “similar to above.” Clearly marked unknowns during re-sync remain questions to resolve.

## Handoff and connectors

A routed plan goes to `chadgrant:implementation`; code quality follows `chadgrant:clean-code`. Use [investigation](../investigation/SKILL.md) for material unknowns about current behavior and [verification](../verification/SKILL.md) for a missing runtime-proof recipe. Preserve IDs and evidence through [handoffs.md](../implementation/handoffs.md). Single self-evident tasks need no routed plan.

Templates carry YAML metadata (`doc`, `title`, `status`, `owner`, `last_synced`, `confluence_page_id`, `jira_project_key`). Preserve existing identifiers and update `last_synced` on changes. Read [connectors.md](connectors.md) only when mapping a doc set to Confluence/Jira; [ROADMAP.md](ROADMAP.md) distinguishes planned integration from built features.
