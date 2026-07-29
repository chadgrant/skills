---
name: refactoring
description: Use when existing code has become a burden — hard to change, duplicated, tangled, or smelling — and you need to improve its structure WITHOUT changing its behavior, safely and in small steps under green tests. Also use before adding a feature to code that makes the change hard ("make the change easy, then make the easy change"). Applies Fowler's Refactoring: the discipline (two hats, tiny reversible steps, tests between each, rule of three), the code-smell catalog, and the named refactorings each smell calls for. Triggers: "refactor this", "clean this up", "this is hard to change", "reduce this debt", "extract a function/class", "this smells", "replace this conditional", "it's become a burden".
---

# Refactoring

Announce at the start: **"Using refactoring: confirm green tests → one small named refactoring at a time → test after each → stop when the burden's gone."**

**Core principle: refactoring changes structure, never behavior — and it's driven by a real burden, not by taste.** You refactor because the code is *now* hard to work with (you're about to add a feature and it fights you; the same change has to be made in three places; a smell is slowing everyone). You do it in **small, reversible steps with the tests green between each**, so at every moment you can stop and ship. This is the pipeline's answer to "something has become debt — rework it into a simpler or more reusable shape."

This composes with the canon: refactoring is *how* you move toward a `design-patterns` pattern or a better `domain-driven-design` aggregate once the need is real; the target state is what `uncle-bob-clean-code` calls clean; the [smell → refactoring catalog](reference.md) is the map.

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

## In the pipeline

Refactoring is a first-class activity, not an afterthought:

- **Planned** — a "reduce burden" refactor is a legitimate `TASK-` in `requirements-driven-planning`, with a verify step of *behavior unchanged (tests green) and the target smell gone*. Debt gets scheduled, not just lamented.
- **Triggered in the build** — when a worker (`clean-implementation`) meets change-friction ("make the change easy" first), or the quality gate / reviewer (`model-routed-delivery`) flags a smell, that spawns a refactoring under the two-hats discipline — kept as its own step/commit, never smuggled into a feature diff.

## Don't over-apply

| Temptation | Reality |
|---|---|
| Refactor the whole module because you're touching one function | Scope to the burden and your path. Sprawling refactors hide behavior changes and blow review. |
| Refactor and add the feature in one commit | Two hats. Separate the diffs so a reviewer can see structure-only vs behavior change. |
| Refactor toward a pattern "for future flexibility" | Rule of three. Move to a pattern when the third real case arrives, not on spec (`design-patterns` over-apply table). |
| Keep polishing past the point of the burden | Stop when the code is easy to change again. Refactoring is means, not end. |

## Red flags — stop if you catch yourself thinking…

| Rationalization | Reality |
|---|---|
| "I'll refactor and fix the bug in the same pass." | Two hats. Refactor to green, commit, *then* change behavior. Mixed diffs hide regressions. |
| "No tests, but I'll be careful." | Careful isn't a safety net. Characterization tests first, or you're editing blind. |
| "I'll just do this one big rename/move across everything." | Big-bang refactors go red in ways you can't localize. Small steps, test between each. |
| "This is the second duplicate — extract it now." | Rule of three. Two is a wince, not yet a pattern; premature extraction is speculative generality. |
| "The whole thing is bad — let me rewrite it while I'm here." | Rewrite is a planned decision with its own risk, not a drive-by. Record it, scope it, get sign-off. |

---

*A discipline-and-catalog layer distilled from **Martin Fowler**'s *Refactoring* (and Michael Feathers' *Working Effectively with Legacy Code* for characterization tests). It is how you move safely toward `design-patterns` and `domain-driven-design` structures, targeting the cleanliness `uncle-bob-clean-code` defines. Full smell → refactoring catalog in [reference.md](reference.md).*
