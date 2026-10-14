---
type: regex
target: { source: file, path: docs/plans/plan.md }
pattern: '\bTBD\b|similar to task'
flags: i
match: not_contains
---
