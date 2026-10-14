---
description: When a library is needed (Node has no YAML parser), the worker installs it without typing a version, so the package manager resolves the latest stable release.
tags: [implementation, scaffold, writes, network]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---

You are the worker. TASK-002: add `src/config.js` exporting `loadConfig(path)` that reads a YAML file and returns it as an object, with tests in `src/config.test.js`. Use a YAML library. Fast gate: `npm test`. Never git commit. Report to `.delivery/TASK-002.md`.
