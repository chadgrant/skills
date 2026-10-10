# skills

A collection of [Agent Skills](https://agentskills.io) for coding agents (Claude Code and any agent supporting the [Agent Skills spec](https://agentskills.io/specification)).

## Skills

Three of these form one pipeline — **plan → implement → review** — so you can spend your day talking requirements and let the software factory build them. One more skill, `chadgrant:clean-code`, sits underneath and holds the standards the pipeline builds and reviews against:

| Skill | Stage | What it does |
| --- | --- | --- |
| [`chadgrant:planning`](skills/planning/) | **Plan** | A planning loop that produces a living family of requirements docs (PRD, ERD, DRD, API contract, UX and ops docs) with small Excalidraw diagrams, kept in sync by a shared ID spine, and a routed implementation plan for the implementation stage. Also re-syncs docs with code, including brownfield repos. Connector-ready for Confluence/Jira. |
| [`chadgrant:implementation`](skills/implementation/) | **Implement** | One skill, two roles, each in its own file so an agent loads only its own. **Orchestrator**: rates each task and routes it to a model tier (asking before using Fable), dispatches full waves of subagents on disjoint files, verifies each wave with one full test and static-gate run, reviews by risk, commits, and escalates stuck tasks; it treats its own context as the budget (one session per milestone, reports on disk, investigation delegated). **Worker**: builds one task verify-first, clean per `chadgrant:clean-code`, UI with Impeccable, services Twelve-Factor, with a debug loop for red tests and a rigorous way to receive review; never commits and never touches shared files. |
| [`chadgrant:code-review`](skills/code-review/) | **Review** | The adversarial reviewer. Six lenses (correctness, security, tests, design, Twelve-Factor, readability), every finding with `file:line` and a breaking case. The design lens prescribes by name ("use a Decorator here", "this needs a Repository") from evidence in the code, and flags patterns to remove. Scoped to a task or feature's files when dispatched by the pipeline; the entire codebase when run on its own. Keeps a `Last full review` stamp in the repo's `AGENTS.md`, and when it goes stale (14 days or 50 commits) the next delivery run or milestone gate reviews the whole codebase. |
| [`chadgrant:clean-code`](skills/clean-code/) | *(standards)* | How to write and review any unit of code well: Robert C. Martin's *Clean Code* + SOLID, the four simplicity rules every other skill cites (**KISS**, **YAGNI**, **DRY**, **convention over configuration**), **Clean Architecture**, and **Construction** (McConnell's *Code Complete*). Its reference files, opened only when the problem calls for one, carry the **Gang of Four** and **Fowler PoEAA** pattern catalogs, **Evans' domain-driven design**, and **Fowler's refactoring** catalog. Applied whenever the agent writes, modifies, or reviews code. |

## Install

These ship as one Claude Code plugin, `chadgrant`:

```sh
claude plugin marketplace add chadgrant/skills
claude plugin install chadgrant@chadgrant-skills
```

Or inside Claude Code: `/plugin install chadgrant --marketplace chadgrant/skills`. The skills then appear as `chadgrant:planning`, `chadgrant:implementation`, `chadgrant:code-review`, and `chadgrant:clean-code`. `claude plugin update chadgrant@chadgrant-skills` picks up new versions.

Other agents supporting the [Agent Skills spec](https://agentskills.io/specification) can copy a folder from `skills/` into their skills directory; the skills refer to each other by their plugin names, so drop the `chadgrant:` prefix there.

Each skill's `SKILL.md` (with its reference files) is the authoritative doc.
