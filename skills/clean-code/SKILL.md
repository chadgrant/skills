---
name: clean-code
description: Apply Clean Code, SOLID, and simplicity principles when writing, modifying, reviewing, or refactoring code, or choosing a design pattern or domain model. Excludes generated, vendored, and explicitly throwaway code.
---

# Clean code

Write code that is easy to read and change. Improve the lines the task touches; keep unrelated cleanup out of scope. Time pressure does not lower the quality bar, and quality does not require speculative machinery.

## Writing rules

- **Functions:** one purpose and one abstraction level; prefer at most three parameters. Replace boolean behavior flags with separate named operations. Separate commands from queries and avoid hidden side effects or input mutation unless mutation is the stated job.
- **Names:** intention-revealing, searchable, and consistent with the domain glossary. Classes are nouns; functions are verbs. Name meaningful constants, e.g. `GOLD_DISCOUNT = 0.15`.
- **Types and boundaries:** represent meaningful IDs and states distinctly where mix-ups cause bugs; derive types from the authoritative schema rather than maintaining copies. Validate untrusted inputs at boundaries and keep invariants in the owning module. Type assertions are not runtime validation; retain checks for mutable state, authorization, and external data.
- **Side effects:** define retry and partial-failure behavior for state-changing operations. Use idempotency keys, transactions, or reconciliation only where the required failure semantics need them; test repeated delivery and interrupted work.
- **Errors:** use the language's idiomatic error mechanism, with diagnostic context. Avoid ambiguous numeric status codes and unexpected nulls; use explicit result/option types or exceptions as appropriate. Preserve existing public contracts.
- **Comments:** explain intent, constraints, warnings, or legal obligations. Rename or extract code that needs a comment explaining what it does. Remove obsolete commented-out code in the area changed.
- **Tests:** prove observable behavior with independent expected values. Test-first where practical; keep tests fast, independent, repeatable, and self-validating, with one concept per test.
- **Conventions:** follow the repo's naming, layout, formatting, and framework defaults without copying defects.

## Design rules

| Principle | Apply it by |
|---|---|
| SRP | Giving each module one reason to change |
| OCP | Adding extension points when real variants need them |
| LSP | Preserving base-type behavior and preconditions in subtypes |
| ISP | Keeping interfaces specific to their clients |
| DIP | Injecting dependencies at genuine I/O or volatile-policy seams |
| KISS | Choosing the simplest design that meets the requirement |
| YAGNI | Omitting hooks, settings, layers, and abstractions without a current caller |
| DRY | Giving each rule, constant, and schema one authoritative home |
| Convention over configuration | Using the stack's standard mechanisms before custom wiring |

Search the repo, framework, and standard library before adding a helper. Reuse an existing implementation at the first occurrence. At the second occurrence of the same cross-cutting concern (logging, retries, timing, caching, authorization, metrics, transactions), use a Decorator or framework middleware.

For business logic, similar text is not necessarily shared knowledge: extract at the third occurrence, or earlier when copies must change together. KISS and YAGNI outrank speculative DRY. A plain function is preferable to an interface with one implementation and no test need, a factory that only calls a constructor, or classes added solely to demonstrate a pattern.

At component scale, dependencies point toward policy, not infrastructure; avoid dependency cycles. For rich domains, keep business invariants in the domain model and draw aggregate boundaries around consistency needs.

## Read only the reference the decision needs

Search headings or pattern names and read the matching section; do not load every catalog for routine coding.

| Need | Reference |
|---|---|
| Worked examples, SOLID, dependency rule, component principles, defensive construction | [reference.md](reference.md) |
| Recurring collaboration, construction, persistence, or presentation problem | [patterns.md](patterns.md): select the minimal pattern and check its “don't use” condition |
| Rich business domain, shared language, consistency boundaries | [domain-driven-design.md](domain-driven-design.md) |
| Behavior-preserving change to tangled or duplicated code | [refactoring.md](refactoring.md): green tests, one small refactoring, re-verify |

## Reviewing code

Check correctness/security, design/simplicity/architecture, then readability. Trace flag combinations and partial side effects; do not let style findings displace bugs. Each finding names a location, concrete consequence, and fix. A pass may have no findings; never invent one to fill a category.

For a requested review or audit, use [code-review](../code-review/SKILL.md) when installed for scope, the nine lenses, and a verdict-first report. Otherwise, use the three passes above within the requested scope and report a verdict (`clean` or blocker/should-fix/nit counts), findings by severity, and any unreviewed areas. Do not run a second overlapping review.
