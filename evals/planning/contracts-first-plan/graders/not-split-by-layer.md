---
type: llm
focus: { source: file, path: docs/plans/plan.md }
---

PASS if the plan has roughly 3 to 15 tasks and each task delivers a cohesive module or part of a feature (for example auth, task management, notifications), rather than one task per layer (a models task, then a repository task, then a routes task) of the same feature.
FAIL if tasks are split by layer, or there are more than 20 tasks.
