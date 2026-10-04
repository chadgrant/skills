---
name: refactoring
description: Use when existing code has become a burden (hard to change, duplicated, tangled, smelly) and its structure must improve without changing its behavior, or before adding a feature to code that makes the change hard. Triggers: "refactor this", "clean this up", "reduce this debt", "extract a function", "this smells", "replace this conditional".
---

# Refactoring

Announce at the start: **"Using refactoring: confirm green tests → one small named refactoring at a time → test after each → stop when the burden's gone."**

**Core principle: refactoring changes structure, never behavior — and it's driven by a real burden, not by taste.** You refactor because the code is *now* hard to work with (you're about to add a feature and it fights you; the same change has to be made in three places; a smell is slowing everyone). You do it in **small, reversible steps with the tests green between each**, so at every moment you can stop and ship. The [smell → refactoring catalog](reference.md) is the map.

## The discipline (do not skip)

1. **Green tests first — or write them.** Refactoring without a test harness is just editing and hoping. If the code isn't covered, add characterization tests that pin current behavior *before* you touch structure.
2. **Two hats — never wear both at once.** You are *either* adding behavior *or* refactoring, never in the same edit. Feature work changes what tests assert; refactoring keeps every test asserting exactly what it did. Switch hats deliberately and know which one you have on.
3. **Small, reversible steps.** Apply one named refactoring (extract function, rename, introduce parameter object…), then run the tests. Then the next. If a step goes red, you moved too far in one go — revert the last step, not the whole session.
4. **Test after every step.** Green → green → green. The safety of refactoring is entirely in the frequency of the check.
5. **Commit at green milestones.** A completed refactoring at green is a natural commit boundary (in the pipeline, the orchestrator commits — `model-routed-delivery`).

## When to refactor — and when not

**Refactor when:**
- **You're about to change code that makes the change hard.** *"Make the change easy (warning: this may be hard), then make the easy change."* — Kent Beck (Fowler builds his "preparatory refactoring" on it). Refactor first, under the refactoring hat; then add the feature under the feature hat.
- **The rule of three.** First time, just do it. Second time you duplicate, wince but proceed. **Third time, refactor** — now the pattern is real, not speculative (this is the honest trigger, the opposite of speculative generality).
- **A smell is slowing work.** A [catalogued smell](reference.md) you keep tripping over earns its refactoring.
- **Comprehension refactoring.** You finally understand a gnarly function — fold that understanding back into its structure and names so the next reader gets it for free.

**Don't refactor when:**
- **You're mid-feature with the feature hat on.** Finish or stash the feature; switch hats cleanly.
- **The code doesn't need to change and isn't in your way.** Ugly-but-stable code that nobody touches is not a priority. Refactor code you're working *in*, not code you happened to notice (Boy Scout Rule applies to your path, not the whole repo).
- **It should be a rewrite, not a refactor.** When the design is beyond incremental repair, that's a planned rewrite decision (record it as an `ADR`/task via `requirements-driven-planning`), not an endless refactor.
- **There are no tests and you can't add them.** Get a characterization harness first; otherwise you're changing behavior blind.

**The four simplicity rules (`uncle-bob-clean-code`) set the direction.** A refactoring should leave the code simpler (KISS), with knowledge in fewer places (DRY, at the third occurrence), with less speculative machinery (YAGNI: deleting an unused abstraction is a refactoring), and closer to the framework's and repo's conventions. A step that adds indirection without removing a burden is going the wrong way.

## In the pipeline

Refactoring is a first-class activity, not an afterthought:

- **Planned** — a "reduce burden" refactor is a legitimate `TASK-` in `requirements-driven-planning`, with a verify step of *behavior unchanged (tests green) and the target smell gone*. Debt gets scheduled, not just lamented.
- **Triggered in the build** — when a worker (`clean-implementation`) meets change-friction ("make the change easy" first), or the quality gate / reviewer (`model-routed-delivery`) flags a smell, that spawns a refactoring under the two-hats discipline — kept as its own step/commit, never smuggled into a feature diff.

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

*Distilled from **Martin Fowler**'s *Refactoring* and Feathers' *Working Effectively with Legacy Code*. Related: `design-patterns` and `domain-driven-design` (the structures you refactor toward), `uncle-bob-clean-code` (what clean means). Smell → refactoring catalog in [reference.md](reference.md).*
