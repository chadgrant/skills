---
description: When the platform already does the job (Intl.DateTimeFormat), the worker adds no dependency.
tags: [implementation, scaffold, writes]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---

You are the worker. TASK-001: add `src/formatDate.js` exporting `formatDate(date, locale)` that returns a date like "October 13, 2026" for `en-US`, with tests in `src/formatDate.test.js`. Fast gate: `npm test`. Never git commit. Report to `.delivery/TASK-001.md`.
