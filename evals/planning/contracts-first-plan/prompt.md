---
description: The plan lists each milestone's contracts (CON-###) before its tasks, sizes tasks as contract groups rather than layers, and records max_parallel.
tags: [planning, writes]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit]
---

The requirements are settled; don't ask me anything, make sensible choices and record them. Write the implementation plan to `docs/plans/plan.md`.

Product: a small HTTP API in TypeScript (Node, Fastify, PostgreSQL) for a team to-do list.
- REQ-001: a user signs up and logs in with email and password.
- REQ-002: a logged-in user creates, edits, completes, and deletes tasks in their team.
- REQ-003: a task can be assigned to a teammate, who gets an email.
- REQ-004: a user lists their team's tasks, filtered by assignee and status.
