# skills

A collection of [Agent Skills](https://agentskills.io) for coding agents (Claude Code and any agent supporting the [Agent Skills spec](https://agentskills.io/specification)).

## Skills

Three of these form one pipeline — **plan → execute → implement** — so you can spend your day talking requirements and let the software factory build them. A **design canon** of four skills sits underneath, composed by the pipeline (and usable standalone) so the code that gets built is designed against the established literature, not invented:

| Skill | Stage | What it does |
| --- | --- | --- |
| [`requirements-driven-planning`](requirements-driven-planning/) | **Plan** | Turns a planning loop into a living, adaptive family of requirements docs — PRD, Engineering Requirements Doc, Data Requirements Doc, API contract, UX/ops docs, Test & QA plan — with digestible Excalidraw diagrams (≤6 boxes, C4-split, ELI5 captions), kept in sync via a shared ID spine, then routes the plan into the build under a *done = green and clean* quality bar (a code-quality gate, not just passing tests). Connector-ready for Confluence/Jira. |
| [`model-routed-execution`](model-routed-execution/) | **Execute** | The software-factory floor manager. Delivers a large multi-task build mostly autonomously: a planner rates each task's difficulty and routes it to a model tier, then a top-tier orchestrator runs waves of subagents (in isolated git worktrees when the blast radius is high), verifying each task is green *and* clean (an independent quality pass over the diff, not just passing tests) before committing it, and escalating a stuck task to a higher tier rather than looping. Consumes the routed plan from `requirements-driven-planning`; hands each task to `clean-implementation`. (Skill name: `model-routed-delivery`.) |
| [`clean-implementation`](clean-implementation/) | **Implement** | The worker's operating manual for building one task well: read the brief, work verify-first, write the code by following the design canon below, build UI with Impeccable, prove it clean as well as green (a quality self-review of the diff), stay in-lane, never commit, report the interface back — plus debug systematically when a test goes red and receive adversarial review with rigor. Portable across a Claude Code subagent or an autonomous "dark factory" node. |
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
