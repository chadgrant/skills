# skills

A collection of [Agent Skills](https://agentskills.io) for coding agents (Claude Code and any agent supporting the [Agent Skills spec](https://agentskills.io/specification)).

## Skills

Three of these form one pipeline — **plan → execute → implement** — so you can spend your day talking requirements and let the software factory build them:

| Skill | Stage | What it does |
| --- | --- | --- |
| [`requirements-driven-planning`](requirements-driven-planning/) | **Plan** | Turns a planning loop into a living, adaptive family of requirements docs — PRD, Engineering Requirements Doc, Data Requirements Doc, API contract, UX/ops docs, Test & QA plan — with digestible Excalidraw diagrams (≤6 boxes, C4-split, ELI5 captions), kept in sync via a shared ID spine, then routes the plan into the build under a *done = green and clean* quality bar (a code-quality gate, not just passing tests). Connector-ready for Confluence/Jira. |
| [`model-routed-execution`](model-routed-execution/) | **Execute** | The software-factory floor manager. Delivers a large multi-task build mostly autonomously: a planner rates each task's difficulty and routes it to a model tier, then a top-tier orchestrator runs waves of subagents (in isolated git worktrees when the blast radius is high), verifying each task is green *and* clean (an independent quality pass over the diff, not just passing tests) before committing it, and escalating a stuck task to a higher tier rather than looping. Consumes the routed plan from `requirements-driven-planning`; hands each task to `clean-implementation`. (Skill name: `model-routed-delivery`.) |
| [`clean-implementation`](clean-implementation/) | **Implement** | The worker's operating manual for building one task well: read the brief, work verify-first, write the code by following `uncle-bob-clean-code`, build UI with Impeccable, prove it clean as well as green (a quality self-review of the diff), stay in-lane, never commit, report the interface back — plus debug systematically when a test goes red and receive adversarial review with rigor. Portable across a Claude Code subagent or an autonomous "dark factory" node. |
| [`uncle-bob-clean-code`](uncle-bob-clean-code/) | *(composed)* | Makes agents write and review code the Uncle Bob way — Robert C. Martin's *Clean Code* teachings and the SOLID principles, applied automatically whenever the agent writes, modifies, or reviews code. `clean-implementation` composes it; also usable standalone for review. |

## Install

Each skill is a self-contained folder. Clone the repo and copy the folder you want into your agent's skills directory:

```sh
git clone https://github.com/chadgrant/skills /tmp/chadgrant-skills
cp -r /tmp/chadgrant-skills/uncle-bob-clean-code ~/.claude/skills/
```

See each skill's own `README.md` for details and per-agent install notes.
