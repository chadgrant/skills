# requirements-driven-planning

An [Agent Skill](https://agentskills.io) that turns a planning loop into a **living family of requirements documents** — a PRD, an Engineering Requirements Doc, and a Data Requirements Doc — then routes an implementation plan into the build. The requirements are the source of truth; the code is downstream of them, and the two are kept in sync by a shared ID spine.

## What it does

- **Adaptive doc set:** always produces a **PRD** (product: problem, users, `REQ-` requirements, success metrics). Adds an **ERD** (engineering: architecture, infra, patterns, *alternatives considered*, `ADR-` decisions) when there's real design, a **DRD** (data: entity model, schemas, data dictionary, PII classification, retention) when the work touches persistent data, an **API contract** when a service/public interface changes, and a **Test & QA plan** when there's non-trivial behavior to prove. A CLI tweak gets a short PRD; a platform gets the whole family.
- **Digestible diagrams:** every structural doc carries **Excalidraw** diagrams held to **≤5–6 boxes each** — bigger systems are split by **C4 zoom level** (Context → Container → Component) instead of crammed — and every diagram gets a plain-language **ELI5 caption**. Boxes are labeled with spine IDs so the diagram stays checkable against the docs.
- **Routed implementation plan:** decomposes the work into atomic `TASK-`s with exact file paths and interpretation-free verify steps, rates each task's difficulty, and assigns a **model tier** — then hands off to the [`multi-model-implementation`](../multi-model-implementation/) (model-routed-delivery) skill to orchestrate the build.
- **Keeps docs in sync:** one shared ID namespace (`REQ- / NFR- / ADR- / ENT- / TASK- / TEST-`) is the spine. A **re-sync** entry path reconciles existing docs against the current code, reports drift (orphan requirements, untraceable tasks, schema/dictionary mismatch, missing PII/retention), and updates them — so the requirements stay true instead of rotting.
- **Connector-ready:** every doc carries machine-readable YAML front-matter, and the spine is the join key for pushing the doc set to a Confluence-style page tree and shredding `REQ-`/`TASK-` into Jira epics/stories. The mapping is specified in [`connectors.md`](connectors.md); live integrations are on the [`ROADMAP.md`](ROADMAP.md), not built yet.

## Files

- [`SKILL.md`](SKILL.md) — the loop: two entry paths (author / re-sync), the adaptive doc-set rules, the diagram discipline, the ID spine, the traceability checklist, connector-readiness, red flags
- [`reference.md`](reference.md) — per-section intent, the anti-patterns that kill each doc type, and which diagram belongs in which doc
- [`connectors.md`](connectors.md) — the Confluence / Jira mapping contract (design; not yet built)
- [`ROADMAP.md`](ROADMAP.md) — what's built now vs. designed-for-later
- [`templates/`](templates/) — fill-in skeletons for [`prd.md`](templates/prd.md), [`erd.md`](templates/erd.md), [`drd.md`](templates/drd.md), [`api-contract.md`](templates/api-contract.md), [`test-qa-plan.md`](templates/test-qa-plan.md), and [`implementation-plan.md`](templates/implementation-plan.md), pre-wired with the ID conventions, connector front-matter, and diagram slots
- [`templates/diagram.excalidraw`](templates/diagram.excalidraw) — a valid 2-box Excalidraw starter scene to clone for each diagram

## How it fits with `multi-model-implementation`

That skill requires a spec/PRD and a routed plan to *exist first*. This skill is the upstream half that produces them: brainstorm-and-clarify → PRD/ERD/DRD → routed implementation plan → hand off. Use them together for an idea-to-shipped pipeline.

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
