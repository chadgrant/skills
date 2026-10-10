# skills

A collection of [Agent Skills](https://agentskills.io) for coding agents (Claude Code and any agent supporting the [Agent Skills spec](https://agentskills.io/specification)).

## Skills

Four of these form one pipeline — **plan → execute → implement → review** — so you can spend your day talking requirements and let the software factory build them. One more skill, `uncle-bob-clean-code`, sits underneath and holds the standards the pipeline builds and reviews against:

| Skill | Stage | What it does |
| --- | --- | --- |
| [`requirements-driven-planning`](requirements-driven-planning/) | **Plan** | A planning loop that produces a living family of requirements docs (PRD, ERD, DRD, API contract, UX and ops docs) with small Excalidraw diagrams, kept in sync by a shared ID spine, and a routed implementation plan for the execute stage. Also re-syncs docs with code, including brownfield repos. Connector-ready for Confluence/Jira. |
| [`model-routed-delivery`](model-routed-delivery/) | **Execute** | The floor manager. Rates each task and routes it to a model tier, dispatches full waves of subagents on disjoint files (bundling easy tasks), verifies each wave with one full test and static-gate run, reviews by risk (a per-task reviewer agent only for the security/money spine, one per wave for other hard tasks, a skim for medium, the gate alone for easy) with reviews pipelined against the next wave, commits, and escalates stuck tasks up a tier. Treats its own context as the budget: one session per milestone resumed from `STATUS.md`, reports on disk with one-line verdicts in context, investigation delegated, one review round with fixes at the task's tier. |
| [`clean-implementation`](clean-implementation/) | **Implement** | The worker's manual for building one task: verify-first, clean code per `uncle-bob-clean-code`, UI with Impeccable, services Twelve-Factor, a debug loop for red tests, a rigorous way to receive review, and a structured report back. Never commits; stays in its lane. |
| [`clean-code-review`](clean-code-review/) | **Review** | The adversarial reviewer. Six lenses (correctness, security, tests, design, Twelve-Factor, readability), every finding with `file:line` and a breaking case. The design lens prescribes by name ("use a Decorator here", "this needs a Repository") from evidence in the code, and flags patterns to remove. Scoped to a task or feature's files when dispatched by the pipeline; the entire codebase when run on its own. Keeps a `Last full review` stamp in the repo's `AGENTS.md`, and when it goes stale (14 days or 50 commits) the next delivery run or milestone gate reviews the whole codebase. |
| [`uncle-bob-clean-code`](uncle-bob-clean-code/) | *(standards)* | How to write and review any unit of code well: Robert C. Martin's *Clean Code* + SOLID, the four simplicity rules every other skill cites (**KISS**, **YAGNI**, **DRY**, **convention over configuration**), **Clean Architecture**, and **Construction** (McConnell's *Code Complete*). Its reference files, opened only when the problem calls for one, carry the **Gang of Four** and **Fowler PoEAA** pattern catalogs, **Evans' domain-driven design**, and **Fowler's refactoring** catalog. Applied whenever the agent writes, modifies, or reviews code. |

## Install

Each skill is a self-contained folder. Clone the repo and copy the folder you want into your agent's skills directory:

```sh
git clone https://github.com/chadgrant/skills /tmp/chadgrant-skills
cp -r /tmp/chadgrant-skills/uncle-bob-clean-code ~/.claude/skills/
```

Each skill's `SKILL.md` (with its `reference.md` where present) is the authoritative doc; `uncle-bob-clean-code` and `requirements-driven-planning` also carry a `README.md` with extra install notes.
