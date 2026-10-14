---
type: regex
target: { source: file, path: docs/requirements/prd.md }
pattern: 'UPDATE|~~|Amends|Change log'
flags: i
match: not_contains
weight: 2
---
