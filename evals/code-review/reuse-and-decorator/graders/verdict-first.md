---
type: llm
---

PASS if the review opens with a one-line verdict giving counts of blockers, should-fix findings, and nits (or the single word "clean"), and its findings cite file names with line numbers or method names.
FAIL if the verdict is missing, comes only at the end, or the findings are prose with no location.
