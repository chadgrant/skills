---
description: Runtime verification preserves evidence and removes only owned scratch state.
tags: [regression, verification]
max_turns: 30
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
---

Use verification to create docs/verification.md for this tiny CLI and prove the create-record journey. Use existing app.py, no dependencies. Do not change app.py. Run the actual CLI in isolated state, assert its JSON response and resulting record, and retain action/results evidence under .delivery/verification/. Exercise the failure command too and record its nonzero status and partial file before cleanup. Clean up your scratch state on both paths. shared-state/ belongs to another run and must remain untouched. Report the actual scope proved; this fixture has no server or database.
