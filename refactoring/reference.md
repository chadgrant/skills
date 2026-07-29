# Refactoring reference — smells → refactorings

Distilled from Fowler's *Refactoring* (2nd ed.). Find the smell you have, apply the named refactoring(s), tests green between each step. Read alongside `SKILL.md`'s two-hats discipline.

---

## Code smells → what to do

| Smell | What it looks like | Refactorings to reach for |
|---|---|---|
| **Mysterious Name** | A name that doesn't say what it is/does | Change Function Declaration, Rename Variable, Rename Field |
| **Duplicated Code** | Same structure in more than one place | Extract Function; Slide Statements then extract; Pull Up Method |
| **Long Function** | A function you scroll, or with comment-delimited sections | Extract Function (the workhorse); Replace Temp with Query; Decompose Conditional; Replace Conditional with Polymorphism |
| **Long Parameter List** | Many params, or params derivable from each other | Introduce Parameter Object; Preserve Whole Object; Replace Parameter with Query |
| **Global / Mutable Data** | Widely-reachable state mutated from afar | Encapsulate Variable; Combine Functions into Class; Encapsulate Collection |
| **Divergent Change** | One module changes for many unrelated reasons | Split Phase; Extract Class (one reason to change each — SRP) |
| **Shotgun Surgery** | One change forces edits across many modules | Move Function/Field; Combine Functions into Class/Module (gather what changes together) |
| **Feature Envy** | A method more interested in another object's data | Move Function; Extract Function then move |
| **Data Clumps** | The same few fields travel together everywhere | Extract Class; Introduce Parameter Object; Preserve Whole Object |
| **Primitive Obsession** | Strings/ints standing in for domain concepts | Replace Primitive with Object (→ Value Object, `domain-driven-design`); Replace Type Code with Subclasses |
| **Repeated Switches** | The same switch/if-on-type in several places | Replace Conditional with Polymorphism; Replace Type Code with Subclasses/State/Strategy (`design-patterns`) |
| **Loops** | Hand-rolled loops obscuring intent | Replace Loop with Pipeline (map/filter/reduce) |
| **Lazy Element** | A class/function that no longer earns its keep | Inline Function; Inline Class; Collapse Hierarchy |
| **Speculative Generality** | Hooks/abstractions for cases that never came | Collapse Hierarchy; Inline Function/Class; Remove Dead Code; Change Function Declaration (drop unused params) |
| **Temporary Field** | A field set only in certain circumstances | Extract Class; Introduce Special Case (Null Object) |
| **Message Chains** | `a.getB().getC().getD()` (Law of Demeter) | Hide Delegate; Extract Function then Move Function |
| **Middle Man** | A class that only delegates onward | Remove Middle Man; Inline Function |
| **Insider Trading** | Modules that know too much of each other's internals | Move Function/Field; Hide Delegate; extract a shared module or use events (`domain-driven-design`) |
| **Large Class** | A class doing too many things (many fields/methods) | Extract Class; Extract Superclass; Replace Type Code with Subclasses |
| **Data Class** | Fields + getters/setters, no behavior | Move Function (move behavior onto it); Encapsulate; often an anemic domain smell (`domain-driven-design`) |
| **Refused Bequest** | A subclass ignoring/overriding much of its parent | Push Down Method/Field; Replace Subclass with Delegate; Replace Superclass with Delegate (LSP) |
| **Comments (as deodorant)** | Comments explaining *what* confusing code does | Extract Function with an intention-revealing name; Rename; Introduce Assertion (keep only why/warning/legal comments — `uncle-bob-clean-code`) |

---

## The core refactorings (the ones you use constantly)

| Refactoring | What it does | Mechanics in one line |
|---|---|---|
| **Extract Function** | Turn a fragment into a named function | Name it for *intent*; move the fragment; pass what it reads, return what it writes; test |
| **Inline Function** | Fold a function back into callers | When the body is as clear as the name and indirection isn't earning its keep |
| **Extract Variable** | Name a subexpression | Introduce an explaining variable for a complex expression; test |
| **Inline Variable** | Remove a variable that adds nothing | When the expression is as clear as the name |
| **Change Function Declaration** | Rename a function or change its parameters | Add the new signature alongside, migrate callers, remove the old (or do it in one go if small) |
| **Encapsulate Variable** | Route access to data through functions | Wrap a field/global in getter/setter (or a small class) so you can control and later restructure it |
| **Rename Variable/Field** | Make a name reveal intent | Small but high-value; do it the moment a name misleads |
| **Introduce Parameter Object** | Replace a recurring group of args with one object | Collapses Data Clumps and Long Parameter Lists; often becomes a Value Object |
| **Combine Functions into Class** | Group functions operating on shared data | When several functions pass the same data around |
| **Combine Functions into Transform** | Derive data via a transform step | For read-derived data computed in many places |
| **Split Phase** | Separate two responsibilities in one block into sequential phases | E.g. parse-then-calculate; each phase gets its own function/structure |
| **Move Function / Move Field** | Relocate to the module that uses/owns it | Fixes Feature Envy, Shotgun Surgery, Insider Trading |
| **Extract Class / Inline Class** | Split a class doing two jobs (or merge one pulling its weight no longer) | SRP in both directions |
| **Decompose Conditional** | Extract condition, then-branch, else-branch into named functions | Turns a dense conditional into readable intent |
| **Replace Nested Conditional with Guard Clauses** | Flatten nesting by returning early on edge cases | The happy path drops to the bottom, unindented |
| **Replace Conditional with Polymorphism** | Move each branch of a type-switch into a subclass/strategy | The canonical fix for Repeated Switches (→ State/Strategy, `design-patterns`) |
| **Replace Type Code with Subclasses / State / Strategy** | Turn a type-code field into a polymorphic hierarchy | When behavior — not just data — varies by the code |
| **Replace Primitive with Object** | Promote a bare primitive to a small typed object | Cures Primitive Obsession; the road to Value Objects |
| **Introduce Special Case (Null Object)** | Replace scattered null/edge checks with a polymorphic case | Cures Temporary Field / repeated null-guards (GoF Special Case) |
| **Separate Query from Modifier** | Split a function that both returns a value and changes state | Command–Query Separation (`uncle-bob-clean-code`) |

---

## Characterization tests (refactoring without a safety net)

When you must refactor untested legacy code (Feathers, *Working Effectively with Legacy Code*):

1. **Pin current behavior.** Write tests that assert what the code *does now* (even if that's arguably wrong) — you're capturing behavior, not judging it.
2. **Find a seam.** A place you can substitute a dependency (inject a fake — DIP, `uncle-bob-clean-code`) so the unit is testable without its real collaborators.
3. **Cover, then change.** Once behavior is pinned, refactor in small steps with the net in place. Fix genuine bugs under the *feature* hat, separately.

---

## How this connects to the rest of the canon

- **`design-patterns`** — most "replace conditional / type code" refactorings land you on a GoF pattern (State, Strategy, Polymorphism, Special Case). Refactor *toward* the pattern when the third case arrives, not before.
- **`domain-driven-design`** — Replace Primitive with Object → Value Objects; Extract Class → tighter aggregates; anemic Data Class is a DDD smell.
- **`uncle-bob-clean-code`** — the target state (small functions, intention-revealing names, CQS, SOLID) is exactly what these refactorings move toward; its red flags are your list of smells to hunt.
- **Pipeline** — planned refactor `TASK-`s in `requirements-driven-planning`; two-hats execution and commit boundaries in `model-routed-delivery`; burden-triggered "make the change easy first" in `clean-implementation`.
