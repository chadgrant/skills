# requirements-driven-planning

An [Agent Skill](https://agentskills.io) that turns a planning loop into a **living family of requirements documents** — product (PRD), engineering (ERD), data (DRD), and, when the work warrants, UX (user flows, wireframes, style guide) and ops (release plan, observability, user docs) — then routes an implementation plan into the build. The requirements are the source of truth; the code is downstream of them, and the two are kept in sync by a shared ID spine.

## What it does

- **Adaptive doc set:** always produces a **PRD** (product: problem, users, `REQ-` requirements, success metrics). Adds an **ERD** (engineering: architecture, infra, patterns, *alternatives considered*, `ADR-` decisions) when there's real design, a **DRD** (data: entity model, schemas, data dictionary, PII classification, retention) when the work touches persistent data, an **API contract** when a service/public interface changes, and a **Test & QA plan** when there's non-trivial behavior to prove. For user-facing work it adds **user flows** + IA, lo-fi **wireframes** (with an interaction spec), and a referenced **style guide** (UI built with the [Impeccable](https://github.com/pbakaus/impeccable) design skill); for prod-facing work, a **release plan** (deploy/migration/rollback), an **observability** doc (SLOs/dashboards/alerts), and **user docs**. Each skipped doc must be justified — a headless API needs no wireframes; a UI that stores data needs a DRD. A CLI tweak gets a short PRD; a platform gets the whole family.
- **Digestible diagrams:** every structural doc carries **Excalidraw** diagrams held to **≤5–6 boxes each** — bigger systems are split by **C4 zoom level** (Context → Container → Component) instead of crammed — and every diagram gets a plain-language **ELI5 caption**. Boxes are labeled with spine IDs so the diagram stays checkable against the docs.
- **Routed implementation plan:** decomposes the work into atomic `TASK-`s with exact file paths and interpretation-free verify steps, rates each task's difficulty, assigns a **model tier**, and sets the definition of *done* — green **and** clean, a code-quality gate rather than passing tests alone — then hands off to the [`model-routed-delivery`](../model-routed-delivery/) skill to orchestrate the build (which in turn dispatches each task to a worker running [`clean-implementation`](../clean-implementation/)).
- **Keeps docs in sync:** one shared ID namespace (`REQ- / NFR- / ADR- / ENT- / NAV- / FLOW- / SCR- / CMP- / TOK- / REL- / SLO- / TASK- / TEST-`) is the spine. Three modes — **author** (whole set up front), **focused-loop** (one doc, one unit at a time, loop until done), and **re-sync** (reconcile docs with the code — a drift check when they exist, or reverse-engineering a brownfield repo into the doc set when they don't, marking `[extracted]` / `[inferred]` / `⚠ needs-confirmation` and never fabricating intent) — keep the requirements true instead of rotting.
- **Connector-ready:** every doc carries machine-readable YAML front-matter, and the spine is the join key for pushing the doc set to a Confluence-style page tree and shredding `REQ-`/`TASK-` into Jira epics/stories. The mapping is specified in [`connectors.md`](connectors.md); live integrations are on the [`ROADMAP.md`](ROADMAP.md), not built yet.

## Files

- [`SKILL.md`](SKILL.md) — the loop: three modes (author / focused-loop / re-sync, which also reverse-engineers a brownfield repo), the adaptive doc-set rules, the diagram discipline, the ID spine, the traceability checklist, connector-readiness, red flags
- [`reference.md`](reference.md) — per-section intent, the anti-patterns that kill each doc type, and which diagram belongs in which doc
- [`connectors.md`](connectors.md) — the Confluence / Jira mapping contract (design; not yet built)
- [`ROADMAP.md`](ROADMAP.md) — what's built now vs. designed-for-later
- [`templates/`](templates/) — fill-in skeletons for [`prd.md`](templates/prd.md), [`erd.md`](templates/erd.md), [`drd.md`](templates/drd.md), [`api-contract.md`](templates/api-contract.md), [`user-flows.md`](templates/user-flows.md), [`wireframes.md`](templates/wireframes.md), [`style-guide.md`](templates/style-guide.md), [`release-plan.md`](templates/release-plan.md), [`observability.md`](templates/observability.md), [`user-docs.md`](templates/user-docs.md), [`test-qa-plan.md`](templates/test-qa-plan.md), and [`implementation-plan.md`](templates/implementation-plan.md), pre-wired with the ID conventions, connector front-matter, and diagram slots
- [`templates/diagram.excalidraw`](templates/diagram.excalidraw) — a valid 2-box Excalidraw starter scene to clone for each diagram

## How it fits: plan → execute → implement

This is the **plan** stage of a three-skill pipeline:

1. **`requirements-driven-planning`** (this skill) — clarify → the requirements doc set (PRD, plus whatever the work warrants) → routed implementation plan → hand off.
2. [`model-routed-delivery`](../model-routed-delivery/) (**execute**) — requires the spec/PRD and routed plan to exist first; runs waves of workers, verifying and committing each task.
3. [`clean-implementation`](../clean-implementation/) (**implement**) — each dispatched worker's manual for building one task well; composes [`uncle-bob-clean-code`](../uncle-bob-clean-code/).

Use them together for an idea-to-shipped pipeline: talk requirements here, let the factory build them.

## Install

This skill lives in the [`chadgrant/skills`](https://github.com/chadgrant/skills) collection under `requirements-driven-planning/`. Clone the repo and copy that folder into your agent's skills directory.

**Claude Code — everywhere (all projects):**

```sh
git clone https://github.com/chadgrant/skills /tmp/chadgrant-skills
cp -r /tmp/chadgrant-skills/requirements-driven-planning ~/.claude/skills/
```

**Claude Code — one project:**

```sh
git clone https://github.com/chadgrant/skills /tmp/chadgrant-skills
cp -r /tmp/chadgrant-skills/requirements-driven-planning .claude/skills/
```

**Other agents:** any agent supporting the [Agent Skills spec](https://agentskills.io/specification) can use this — copy the `requirements-driven-planning/` folder into that agent's skills directory.

The skill triggers automatically on its description when you ask to write a PRD, spec something out, or keep requirements in sync.

## Attribution

Grounded in Google's design-doc structure (Malte Ubl), Amazon's working-backwards PR/FAQ, Nygard-style ADRs, and standard data-dictionary/PII-governance practice. Inspired by the brainstorm-before-code discipline of [obra/superpowers](https://github.com/obra/superpowers).
