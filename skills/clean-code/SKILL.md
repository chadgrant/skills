---
name: clean-code
description: Use when writing, modifying, or refactoring code in any language, or when reviewing code, a diff, or a pull request — before the first line is written and before review feedback is sent. Also when a design problem appears: a growing conditional, swappable behavior, where domain logic or data access lives, modeling a business domain, or code that has become hard to change. Triggers: "which pattern", "GoF", "strategy vs state", "repository vs active record", "domain model", "DDD", "bounded context", "aggregate", "refactor this", "clean this up", "this smells".
---

# Uncle Bob Clean Code

## Overview

Write and review all code the way Robert C. Martin (Uncle Bob) teaches in *Clean Code* and *Agile Software Development*: code that reads like well-written prose, does one thing per unit, and depends on abstractions at genuine seams.

**Core principle: the only way to go fast is to go well.** Code is read far more often than it is written — optimize for the next reader. There is no "quick version" that skips these rules; the quick version IS the clean version.

**Boy Scout Rule:** leave every file cleaner than you found it.

## When to Use

- Writing any new function, class, or module
- Modifying or refactoring existing code
- Reviewing code: PRs, diffs, "does this look OK?"

Not for: vendored or generated code, or scripts the user explicitly calls throwaway.

## Writing Code

**Functions**
- Small — each does ONE thing, at one level of abstraction. Extract until it reads like prose.
- ≤ 3 parameters. Never boolean/flag parameters — write two functions instead.
- No hidden side effects. Command–query separation: change state OR answer a question, never both.
- Don't mutate inputs unless mutation is the function's stated job.

**Names**
- Intention-revealing, pronounceable, searchable: `discountRate`, not `d` or `r`.
- Classes are nouns, functions are verbs. One word per concept per codebase.
- Name every magic number: `GOLD_DISCOUNT = 0.15`.

**Errors**
- Throw exceptions; never return status codes (`0`/`-1`). Never return or pass null — use empty collections, option types, or throw.
- Error messages carry enough context to diagnose without a debugger.

**Comments**
- A comment compensates for failure to express it in code — rename or extract instead.
- Delete commented-out code on sight. Keep only intent, warning, or legal comments that code cannot express.

**Tests**
- Test-first where the environment allows (Three Laws of TDD). Tests follow FIRST: Fast, Independent, Repeatable, Self-validating, Timely. One concept per test. Test code is held to production standards.

**SOLID** — the table below is the working rule. [reference.md](reference.md) holds worked examples, **Clean Architecture** (the Dependency Rule; component cohesion REP/CCP/CRP and coupling ADP/SDP/SAP) and **Construction** (Code Complete: defensive programming, functional cohesion, table-driven methods); open the section a review pass or design decision calls for.

| Principle | Rule | Violation smell |
|---|---|---|
| SRP | One reason to change per class/module | A class that computes AND persists AND notifies |
| OCP | Extend behavior without editing working code | if/else or switch on a type code, especially duplicated |
| LSP | Subtypes substitutable for their base type | Override that throws or strengthens preconditions |
| ISP | Small, client-specific interfaces | Implementers with empty or stub methods |
| DIP | Depend on abstractions at seams | Business logic constructing its own DB/network/clock |

**Simplicity**: four rules that outrank cleverness. Sibling skills cite them by name.

| Principle | Rule | Violation smell |
|---|---|---|
| KISS | The simplest design that passes the tests and reads clearly wins | A layer, indirection, or generic mechanism that a plain function would replace |
| YAGNI | Build what today's requirement needs; extend when the second real case arrives | A hook, option, parameter, or abstraction with no current caller |
| DRY | Every piece of knowledge has one authoritative home | The same rule, constant, or schema edited in several places |
| Convention over configuration | Follow the language's, framework's, and repo's standard layout, naming, and defaults; configure only where you truly differ | A setting nobody varies; a home-made mechanism where the framework has a standard one; wiring a naming convention would make unnecessary |

Where they pull apart: code that looks alike but changes for different reasons is not duplication, so KISS and YAGNI outrank DRY until the third occurrence (the rule of three, [refactoring.md](refactoring.md)). Convention decides how few settings exist; the ones that remain still come from the environment (Twelve-Factor).

**Existing messy codebase?** Match its conventions — naming case, formatting, module layout — never its defects. "Match our style" means style, not smells: single-letter names, status-code returns, and blob functions are defects, not style. Apply the Boy Scout Rule to lines you touch; don't launch drive-by rewrites of code the task doesn't touch.

## Design problems: open the file the problem calls for

The rules above cover any unit of code. Three files in this skill carry the design knowledge above that altitude. Each holds its discipline, its over-apply table, and its catalog; read the one the problem names and don't reinvent what it catalogs.

| The problem | Open | The rule that matters most |
|---|---|---|
| A recurring design problem: a growing conditional, swappable behavior, complex construction, adapting an interface, where domain logic, data access, or the web layer lives | [patterns.md](patterns.md) (Gang of Four, Fowler's PoEAA) | Name the problem before the pattern; apply the minimal form; use the framework's version when it ships one; reject the pattern when the problem isn't there |
| Modeling a rich, changing business domain: the language, the boundaries, what must stay consistent | [domain-driven-design.md](domain-driven-design.md) (Evans) | The code uses the domain experts' words; aggregates are small and drawn around invariants; one transaction, one aggregate; the domain depends on nothing |
| Code that has become a burden: hard to change, duplicated, tangled | [refactoring.md](refactoring.md) (Fowler's smell → refactoring catalog) | Green tests first; two hats, never both in one edit; one small named refactoring, then run the tests; rule of three |

## Reviewing Code

Run three REQUIRED passes and report findings in this order. A review that contains only one kind of finding means a pass was skipped.

1. **Correctness & security** — bugs, injection, resource leaks, error paths, concurrency. Trace every boolean-flag combination end to end: a flag that only partially gates behavior (a "dry run" that still sends email) is a bug here, not just a design smell. Never let design commentary crowd these out.
2. **Design (SOLID + simplicity + architecture pass)** — walk the SOLID table and the simplicity table (KISS, YAGNI, DRY, convention over configuration) above against the diff, plus: flag arguments, functions doing several things, hidden side effects, train wrecks (`a.getB().getC().doIt()` — Law of Demeter), null returns/params, switch-on-type. At component scale, check the **Dependency Rule** (does policy depend on a detail? any dependency cycles?) and whether a **known pattern is missing or misapplied** ([patterns.md](patterns.md)), or the **domain model is anemic / an aggregate leaks** ([domain-driven-design.md](domain-driven-design.md)). Where a smell is real, name the **refactoring** that fixes it ([refactoring.md](refactoring.md)).
3. **Readability** — names, magic numbers, commented-out code, comment quality, duplication (DRY).

Reviewing someone else's work or auditing a codebase? `chadgrant:code-review` wraps these passes in a full procedure: scope, security and Twelve-Factor checklists, a test lens, and the report format.

For each finding: name the principle or smell, say concretely why it will hurt, and sketch the fix. End with an explicit verdict: blockers, should-fix, nits.

## Don't Over-Apply — this is also Uncle Bob

Needless complexity is itself a smell.

| Temptation | Reality |
|---|---|
| Interface or abstract base for every class "for DIP" | Abstract only at genuine seams (I/O, volatile policy). One implementation and no test need = no interface. |
| Class explosion: twelve one-method classes for a 40-line feature | SRP means one reason to change, not one function per class. Plain functions are fine. |
| Design-pattern showcase | Patterns are vocabulary for problems you HAVE, not decoration. |
| Speculative hooks and config "for later" | YAGNI. Extend when the second case arrives — that is OCP's moment, not before. |
| Extracting a shared helper from two look-alike snippets "for DRY" | DRY is about knowledge, not text. Wait for the third occurrence, and check they change for the same reason. |
| A custom project layout, config format, or wiring scheme | Convention over configuration. The framework's standard way is the one the next reader already knows. |

## Rationalization Table

| Excuse | Reality |
|---|---|
| "No time — demo in 20 minutes" | Decomposed code with real names takes the same minutes to write and fewer to debug. Going well is going fast. |
| "Match the existing style" | Conventions yes, defects no. Nobody asked you to replicate their bugs' aesthetics. |
| "Don't gold-plate it" | Named functions and thrown exceptions are the floor, not gold-plating. Gold-plating is speculative abstraction — see the over-apply table. |
| "It's a small script" | Small scripts become load-bearing. If it's truly throwaway, the user will say so. |
| "Tests pass, it works in staging" | Passing tests don't catch injection, leaks, or LSP traps. Run all three review passes. |
| "They just want an LGTM" | An LGTM you don't believe is a defect you co-signed. |
| "I'll clean it up after it works" | "Later" has no slot on the schedule. Write it clean the first time. |

## Red Flags — stop and fix before delivering

- A function whose sections you'd separate with blank lines and comments → extract those sections
- A parameter named `flag`, `mode`, `dry`, or any boolean argument
- `return -1` / `return 0` as status, or `return null`
- A name of ≤ 2 letters outside a trivial loop index
- You typed a comment explaining WHAT the next lines do
- A review with only style nits or only bug findings — a pass was skipped
