# skills

A collection of [Agent Skills](https://agentskills.io) for coding agents (Claude Code and any agent supporting the [Agent Skills spec](https://agentskills.io/specification)).

## Skills

| Skill | What it does |
| --- | --- |
| [`uncle-bob-clean-code`](uncle-bob-clean-code/) | Makes agents write and review code the Uncle Bob way — Robert C. Martin's *Clean Code* teachings and the SOLID principles, applied automatically whenever the agent writes, modifies, or reviews code. |

## Install

Each skill is a self-contained folder. Clone the repo and copy the folder you want into your agent's skills directory:

```sh
git clone https://github.com/chadgrant/skills /tmp/chadgrant-skills
cp -r /tmp/chadgrant-skills/uncle-bob-clean-code ~/.claude/skills/
```

See each skill's own `README.md` for details and per-agent install notes.
