# skills

A collection of [Agent Skills](https://agentskills.io) for coding agents (Claude Code and any agent supporting the [Agent Skills spec](https://agentskills.io/specification)).

## Skills

Three of these form one pipeline — **plan → execute → implement** — so you can spend your day talking requirements and let the software factory build them. A **design canon** of four skills sits underneath, composed by the pipeline (and usable standalone) so the code that gets built is designed against the established literature, not invented:

| Skill | Stage | What it does |
| --- | --- | --- |
| [`requirements-driven-planning`](requirements-driven-planning/) | **Plan** | A planning loop that produces a living family of requirements docs (PRD, ERD, DRD, API contract, UX and ops docs) with small Excalidraw diagrams, kept in sync by a shared ID spine, and a routed implementation plan for the execute stage. Also re-syncs docs with code, including brownfield repos. Connector-ready for Confluence/Jira. |
| [`model-routed-delivery`](model-routed-delivery/) | **Execute** | The floor manager. Rates each task and routes it to a model tier, dispatches full waves of subagents on disjoint files, verifies each result is green and clean, reviews by risk (per-task only for the security/money spine, per-wave for other hard tasks, none for the rest) with reviews pipelined against the next wave, commits, and escalates stuck tasks up a tier. |
| [`clean-implementation`](clean-implementation/) | **Implement** | The worker's manual for building one task: verify-first, clean code per the canon below, UI with Impeccable, services Twelve-Factor, a debug loop for red tests, a rigorous way to receive review, and a structured report back. Never commits; stays in its lane. |
| [`uncle-bob-clean-code`](uncle-bob-clean-code/) | *(canon)* | How to write and review any unit of code well: Robert C. Martin's *Clean Code* + SOLID, **Clean Architecture** (dependency rule, component cohesion/coupling), and **Construction** (McConnell's *Code Complete*). Applied whenever the agent writes, modifies, or reviews code. |
| [`design-patterns`](design-patterns/) | *(canon)* | Name a recurring design problem → the proven solution from the **Gang of Four** (creational/structural/behavioral) and **Fowler's PoEAA** (domain logic, data source, O/R, web, distribution, concurrency) — and when *not* to reach for one. |
| [`domain-driven-design`](domain-driven-design/) | *(canon)* | Model a rich domain with **Evans' DDD**: ubiquitous language, bounded contexts, context mapping (strategic); entities, value objects, aggregates and invariants, repositories, domain events (tactical). |
| [`refactoring`](refactoring/) | *(canon)* | Improve structure without changing behavior when code has become a burden: **Fowler's** smell → refactoring catalog plus the discipline (two hats, small steps under green tests, rule of three). Woven into the pipeline as a first-class activity. |

## Install

Each skill is a self-contained folder. Clone the repo and copy the folder you want into your agent's skills directory:

```sh
git clone https://github.com/chadgrant/skills /tmp/chadgrant-skills
cp -r /tmp/chadgrant-skills/uncle-bob-clean-code ~/.claude/skills/
```

Each skill's `SKILL.md` (with its `reference.md` where present) is the authoritative doc; `uncle-bob-clean-code` and `requirements-driven-planning` also carry a `README.md` with extra install notes.
