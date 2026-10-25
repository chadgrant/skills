---
description: Host adapters preserve worktree and role boundaries without assuming Claude tool names.
tags: [regression, implementation]
max_turns: 12
allowed_tools: [Skill, Read]
---

Using implementation's delegation and host guidance, describe dispatch for one authorized Codex worker (do not actually spawn it). This hypothetical host exposes spawn_agent(message, fork_turns), where fork_turns accepts all or none; it exposes followup_task and no Agent tool or automatic worktree isolation. The parent context contains the plan. TASK-004 may edit src/parser.py and its tests; base is the supplied integration SHA; fast gate is `python3 -m unittest`; report path is /workspace/reports/TASK-004.md. It must not alter frozen contracts. A structured question tool is available. Show the brief and prerequisites, without inventing model or tool fields.
