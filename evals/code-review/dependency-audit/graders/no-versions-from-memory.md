---
type: llm
---

PASS if, wherever the review states a dependency's current latest version, it either says the version must be looked up in the registry (or names the lookup command) or says it could not check.
FAIL if it states "the latest version is X" for a package as fact without any lookup or caveat.
