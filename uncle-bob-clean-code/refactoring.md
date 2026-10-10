# Refactoring

**Core principle: refactoring changes structure, never behavior — and it's driven by a real burden, not by taste.** You refactor because the code is *now* hard to work with (you're about to add a feature and it fights you; the same change has to be made in three places; a smell is slowing everyone). You do it in **small, reversible steps with the tests green between each**, so at every moment you can stop and ship. The smell → refactoring catalog below is the map.

## The discipline (do not skip)

1. **Green tests first — or write them.** Refactoring without a test harness is just editing and hoping. If the code isn't covered, add characterization tests that pin current behavior *before* you touch structure.
2. **Two hats — never wear both at once.** You are *either* adding behavior *or* refactoring, never in the same edit. Feature work changes what tests assert; refactoring keeps every test asserting exactly what it did. Switch hats deliberately and know which one you have on.
3. **Small, reversible steps.** Apply one named refactoring (extract function, rename, introduce parameter object…), then run the tests. Then the next. If a step goes red, you moved too far in one go — revert the last step, not the whole session.
4. **Test after every step.** Green → green → green. The safety of refactoring is entirely in the frequency of the check.
5. **Commit at green milestones.** A completed refactoring at green is a natural commit boundary (in the pipeline, the orchestrator commits — `implementation`).

## When to refactor — and when not

**Refactor when:**
- **You're about to change code that makes the change hard.** *"Make the change easy (warning: this may be hard), then make the easy change."* — Kent Beck (Fowler builds his "preparatory refactoring" on it). Refactor first, under the refactoring hat; then add the feature under the feature hat.
- **The rule of three.** First time, just do it. Second time you duplicate, wince but proceed. **Third time, refactor** — now the pattern is real, not speculative (this is the honest trigger, the opposite of speculative generality).
- **A smell is slowing work.** A catalogued smell (below) you keep tripping over earns its refactoring.
- **Comprehension refactoring.** You finally understand a gnarly function — fold that understanding back into its structure and names so the next reader gets it for free.

**Don't refactor when:**
- **You're mid-feature with the feature hat on.** Finish or stash the feature; switch hats cleanly.
- **The code doesn't need to change and isn't in your way.** Ugly-but-stable code that nobody touches is not a priority. Refactor code you're working *in*, not code you happened to notice (Boy Scout Rule applies to your path, not the whole repo).
- **It should be a rewrite, not a refactor.** When the design is beyond incremental repair, that's a planned rewrite decision (record it as an `ADR`/task via `planning`), not an endless refactor.
- **There are no tests and you can't add them.** Get a characterization harness first; otherwise you're changing behavior blind.

**The four simplicity rules ([SKILL.md](SKILL.md)) set the direction.** A refactoring should leave the code simpler (KISS), with knowledge in fewer places (DRY, at the third occurrence), with less speculative machinery (YAGNI: deleting an unused abstraction is a refactoring), and closer to the framework's and repo's conventions. A step that adds indirection without removing a burden is going the wrong way.

## In the pipeline

Refactoring is a first-class activity, not an afterthought:

- **Planned** — a "reduce burden" refactor is a legitimate `TASK-` in `planning`, with a verify step of *behavior unchanged (tests green) and the target smell gone*. Debt gets scheduled, not just lamented.
- **Triggered in the build** — when an `implementation` worker meets change-friction ("make the change easy" first), or the quality gate or a `clean-code-review` reviewer flags a smell, that spawns a refactoring under the two-hats discipline — kept as its own step/commit, never smuggled into a feature diff.

## Red flags: don't over-apply

| Thought | Reality |
|---|---|
| "I'll refactor and fix the bug / add the feature in the same pass." | Two hats. Refactor to green, commit, *then* change behavior. Mixed diffs hide regressions. |
| "No tests, but I'll be careful." | Careful isn't a safety net. Characterization tests first, or you're editing blind. |
| "One big rename / move across everything." | Big-bang refactors go red in ways you can't localize. Small steps, test between each. |
| "Second duplicate; extract it now." / "Toward a pattern for future flexibility." | Rule of three. Two is a wince, not a pattern; premature extraction is speculative generality. |
| "I'm touching one function; refactor the whole module." | Scope to the burden and your path. Sprawling refactors hide behavior changes and blow up review. |
| "The whole thing is bad; rewrite it while I'm here." | A rewrite is a planned decision with its own risk. Record it as an `ADR`, scope it, get sign-off. |
| "A bit more polish." | Stop when the code is easy to change again. Refactoring is a means, not an end. |

---

## Catalog

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
| **Primitive Obsession** | Strings/ints standing in for domain concepts | Replace Primitive with Object (→ Value Object, [domain-driven-design.md](domain-driven-design.md)); Replace Type Code with Subclasses |
| **Repeated Switches** | The same switch/if-on-type in several places | Replace Conditional with Polymorphism; Replace Type Code with Subclasses/State/Strategy ([patterns.md](patterns.md)) |
| **Loops** | Hand-rolled loops obscuring intent | Replace Loop with Pipeline (map/filter/reduce) |
| **Lazy Element** | A class/function that no longer earns its keep | Inline Function; Inline Class; Collapse Hierarchy |
| **Speculative Generality** | Hooks/abstractions for cases that never came | Collapse Hierarchy; Inline Function/Class; Remove Dead Code; Change Function Declaration (drop unused params) |
| **Temporary Field** | A field set only in certain circumstances | Extract Class; Introduce Special Case (Null Object) |
| **Message Chains** | `a.getB().getC().getD()` (Law of Demeter) | Hide Delegate; Extract Function then Move Function |
| **Middle Man** | A class that only delegates onward | Remove Middle Man; Inline Function |
| **Insider Trading** | Modules that know too much of each other's internals | Move Function/Field; Hide Delegate; extract a shared module or use events ([domain-driven-design.md](domain-driven-design.md)) |
| **Large Class** | A class doing too many things (many fields/methods) | Extract Class; Extract Superclass; Replace Type Code with Subclasses |
| **Data Class** | Fields + getters/setters, no behavior | Move Function (move behavior onto it); Encapsulate; often an anemic domain smell ([domain-driven-design.md](domain-driven-design.md)) |
| **Refused Bequest** | A subclass ignoring/overriding much of its parent | Push Down Method/Field; Replace Subclass with Delegate; Replace Superclass with Delegate (LSP) |
| **Comments (as deodorant)** | Comments explaining *what* confusing code does | Extract Function with an intention-revealing name; Rename; Introduce Assertion (keep only why/warning/legal comments — [SKILL.md](SKILL.md)) |

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
| **Replace Conditional with Polymorphism** | Move each branch of a type-switch into a subclass/strategy | The canonical fix for Repeated Switches (→ State/Strategy, [patterns.md](patterns.md)) |
| **Replace Type Code with Subclasses / State / Strategy** | Turn a type-code field into a polymorphic hierarchy | When behavior — not just data — varies by the code |
| **Replace Primitive with Object** | Promote a bare primitive to a small typed object | Cures Primitive Obsession; the road to Value Objects |
| **Introduce Special Case (Null Object)** | Replace scattered null/edge checks with a polymorphic case | Cures Temporary Field / repeated null-guards (GoF Special Case) |
| **Separate Query from Modifier** | Split a function that both returns a value and changes state | Command–Query Separation ([SKILL.md](SKILL.md)) |

---

## Characterization tests (refactoring without a safety net)

When you must refactor untested legacy code (Feathers, *Working Effectively with Legacy Code*):

1. **Pin current behavior.** Write tests that assert what the code *does now* (even if that's arguably wrong) — you're capturing behavior, not judging it.
2. **Find a seam.** A place you can substitute a dependency (inject a fake — DIP, [SKILL.md](SKILL.md)) so the unit is testable without its real collaborators.
3. **Cover, then change.** Once behavior is pinned, refactor in small steps with the net in place. Fix genuine bugs under the *feature* hat, separately.
