---
type: regex
target: last_message
pattern: '\b(dryRun|dry_run|isDryRun|preview|simulate)\s*[?]?\s*:\s*boolean'
flags: i
match: not_contains
---
