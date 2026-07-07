# skills

A collection of [Agent Skills](https://agentskills.io) for coding agents (Claude Code and any agent supporting the [Agent Skills spec](https://agentskills.io/specification)).

## Skills

| Skill | What it does |
| --- | --- |
| [`uncle-bob-clean-code`](uncle-bob-clean-code/) | Makes agents write and review code the Uncle Bob way — Robert C. Martin's *Clean Code* teachings and the SOLID principles, applied automatically whenever the agent writes, modifies, or reviews code. |
| [`requirements-driven-planning`](requirements-driven-planning/) | Turns a planning loop into a living, adaptive family of requirements docs — PRD, Engineering Requirements Doc, Data Requirements Doc, API contract, Test & QA plan — with digestible Excalidraw diagrams (≤6 boxes, C4-split, ELI5 captions), kept in sync via a shared ID spine, then routes the plan into the build. Connector-ready for Confluence/Jira. |
| [`multi-model-implementation`](multi-model-implementation/) | Delivers a large multi-task build mostly autonomously: a planner rates each task's difficulty and routes it to a model tier, then a top-tier orchestrator runs waves of subagents on disjoint files, verifying and committing each task. Consumes the spec/plan produced by `requirements-driven-planning`. |

## Install

Each skill is a self-contained folder. Clone the repo and copy the folder you want into your agent's skills directory:

```sh
git clone https://github.com/chadgrant/skills /tmp/chadgrant-skills
cp -r /tmp/chadgrant-skills/uncle-bob-clean-code ~/.claude/skills/
```

See each skill's own `README.md` for details and per-agent install notes.
