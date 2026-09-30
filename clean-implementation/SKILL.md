---
name: clean-implementation
description: Use when building a single task from a plan — the worker's operating manual for turning one task brief into verified, clean, committed-ready code. Applies whether you're a Claude Code subagent dispatched by model-routed-delivery or an autonomous "dark factory" node. Understand the task and its interface contract, work verify-first, write the code by following the uncle-bob-clean-code skill (composing design-patterns and domain-driven-design for design decisions, and refactoring when existing code has become a burden), build UI with Impeccable against the style guide, stay in your assigned files, never commit, and report the interface you produced back to the orchestrator. Prove the code clean as well as green — an uncle-bob self-review of your own diff (one thing per function, no bloat, design patterns only where warranted), because passing tests are necessary but not sufficient. When a test goes red, debug systematically instead of thrashing, and escalate at your ceiling; when adversarial review comes back, receive it with rigor — verify each finding, fix the root, push back on wrong notes, never performatively agree. Triggers: "implement TASK-###", "build this task", a dispatched task brief, "you are the worker", "the test is failing", "address the review".
---

# Clean implementation

Announce at the start: **"Using clean-implementation: read the brief → verify-first → write it clean → prove it green *and* clean → report back."** (Red bar → debug systematically; review back → receive with rigor.)

**Core principle: your job is one task, done well and proven — not the whole system.** You are a **worker**, not the orchestrator. Someone above you decomposed the work, routed this task to you, and will verify, commit, and integrate your result. Your entire contract is: build exactly the task in your brief, make its verify step pass, and hand back a truthful report. Doing more, touching more, or claiming more is a defect.

This is the **implementation** end of the pipeline (`requirements-driven-planning` → `model-routed-delivery` → **`clean-implementation`**). The layer above owns routing, waves, commits, and the ledger. You own the keystrokes for one unit of work.

## Your input: the task brief

A well-formed brief gives you everything you need. Confirm you have it before typing:

- **Task id + goal** — the one thing this task delivers.
- **Files** — exactly which to create / modify / test. This set is your lane; it is disjoint from every other in-flight worker's lane on purpose.
- **Interface to produce** — the signatures, types, or contract later tasks depend on. This is a promise; match it exactly.
- **Verify step** — the exact build/test command that proves the task done, needing no human interpretation.
- **Difficulty / `observe` flag**: if flagged `observe`, expect a dedicated adversarial review of your result. A Hard task without the flag is reviewed with the rest of its wave. Either way, write to survive it.
- **Global constraints** — stack, fail-mode, and (for UI work) the Impeccable + style-guide constraint, copied verbatim from the plan.

**Missing or ambiguous brief?** Don't guess your way past a genuine fork — a wrong assumption here becomes wrong code the orchestrator has to catch and unwind. State the ambiguity in your report and, where you can, proceed on the smallest defensible interpretation and flag it `⚠`. Never invent an interface the plan didn't specify.

## The build loop

1. **Read the task and its interface contract first.** Know what you must produce and what you may depend on before you write a line. Read the files in your lane and the interfaces of the tasks yours depends on — not the whole tree.
2. **Verify-first.** Where the environment allows, write the failing test from the verify step before the implementation (uncle-bob's Three Laws of TDD). The verify step is the target; make it fail for the right reason, then make it pass.
3. **Write the code by following the `uncle-bob-clean-code` skill.** That skill is this skill's code-quality doctrine — small single-purpose functions, intention-revealing names, exceptions over status codes, no flag arguments, SOLID at genuine seams, Clean Architecture's dependency rule, and its own "don't over-apply" guardrails. Do not restate or second-guess it; invoke it and follow it. The Boy Scout Rule applies to lines you touch — and only those. **When the task involves a design decision** — how objects collaborate, how the domain is modeled, how a layer is structured — also compose **`design-patterns`** (reach for a known GoF / Fowler-PoEAA solution, don't invent) and, for a rich domain, **`domain-driven-design`**. **If the code you must change has become a burden**, make the change easy first: refactor under green tests via **`refactoring`** (two hats — refactor, *then* add the feature; never smuggle a refactor into the feature diff).
4. **UI/site work → build with Impeccable.** If the task has a user-facing surface, build it with the [Impeccable](https://github.com/pbakaus/impeccable) skill against the design system's `TOK-`/`CMP-` from the project's style guide (`design-system/style-guide.md`), per the plan's global constraint. Lo-fi wireframes define layout; the style guide defines visual language; Impeccable is how it gets built.
5. **Prove it green.** Run your task's exact verify step **yourself**. The task is not done until its `TEST-` passes for the right reason. A worker who reports "done" on unrun tests has handed the orchestrator a live grenade. **Red instead of green? Don't guess — drop to the debug loop below.**
6. **Prove it clean, not just green.** Green tests are necessary, not sufficient. Run `uncle-bob-clean-code`'s three passes over *your own* diff — correctness, design (SOLID), readability — and confirm the code is genuinely *good*: one thing per function, no needless abstraction or speculative hooks, no duplication, and **no bloat** — uncle-bob's "don't over-apply" guardrails name these smells directly (needless complexity, class explosion, speculative hooks, design-pattern showcase). Design patterns appear only where the problem demands one, never as decoration. A task that passes its test but reads like a mess is **not done**. Fix what the pass surfaces, then re-verify green.
7. **Report back** (see format below). Your final message is a structured report to the orchestrator, not prose for a human.

## When a test goes red — debug systematically, don't thrash

A failing verify step is a clue, not a cue to start guessing. Random edits until the bar turns green produce code that passes for reasons you can't name — the worst thing to hand an orchestrator.

1. **Reproduce it reliably.** Run the failing step until you can trigger the failure on demand. A failure you can't reproduce, you can't fix — report it as flaky; never paper over it.
2. **Read the actual error.** The stack trace / assertion diff names the symptom. Resist "I bet it's X" before you've read what it actually says.
3. **One hypothesis at a time.** State what you think is wrong and *why*, then test that one thing. Change three things at once and a green bar tells you nothing.
4. **Find the root cause, not the symptom.** Ask why the failing value is wrong, then why *that* is — until you reach the actual defect. A swallowed exception, a `+1` that hides an off-by-one, a retry that masks a race: those are symptom-patches, and the orchestrator's `observe` pass will find what you buried.
5. **Minimal fix, then re-verify for the right reason.** Fix the root cause with the smallest change, rerun the verify step, and confirm it passes *because the defect is gone* — not because you weakened the test.
6. **Ceiling: stop and escalate.** If you've formed and tested a few hypotheses and it's still red — or the real fix needs a file outside your lane — **stop and report the failure to the orchestrator** with what you tried and ruled out. Thrashing past your competence burns tokens and buries the real issue. Escalation is not failure; a silent wrong "fix" is.

## When review comes back — receive it with rigor

If your task was reviewed (a dedicated `observe` review, or the wave-level review of Hard tasks), an adversarial reviewer will try to refute it. Two failure modes are equally bad: caving to every note, and dismissing all of them. Neither is engineering.

1. **Verify each finding before you touch code.** Reproduce the failure the reviewer claims. A finding you can reproduce is real — act on it. A finding you cannot is a claim to check, not an order to obey.
2. **Fix what's real at the root** (via the debug loop above) — never a patch that silences the reviewer's specific example while leaving the defect.
3. **Push back with evidence, not deference.** If a suggestion is wrong or would break an invariant, say so and show why — the failing case it would introduce, the requirement it violates. "Good catch, will do" on a note you haven't verified is how a wrong fix ships with two names on it.
4. **Never performatively agree.** Blindly implementing feedback is as much an abdication as ignoring it. The reviewer is a second set of eyes, not an authority whose word skips verification.
5. **Report your response.** For each finding: real → fixed (with the re-verify evidence), or refuted → why (with the case that proves it). The orchestrator adjudicates on evidence, not politeness.

## Worker iron rules (the orchestrator is counting on these)

- **Stay in your lane.** Touch only the files in your brief. Waves run in parallel on disjoint paths — a stray edit outside your set clobbers another worker and corrupts the whole wave. Need a file that isn't yours? Report it; don't reach for it.
- **Never `git commit`.** Committing is the orchestrator's job, one commit per verified task, after it verifies independently. You produce the change; you do not record it. This holds even if you're certain it's correct.
- **Verify your own work before reporting.** Never report "tests pass" on a test you didn't run. Run the verify step and paste what happened.
- **Honest environment ceiling.** If the sandbox can't fully exercise the task (needs real cloud, signing certs, live services), "done" means **code-complete + tested-with-fakes + a runbook for the real-environment step** — say exactly that. Never imply production-verified work you couldn't run.
- **Match the codebase's conventions, not its defects.** (uncle-bob's rule — naming case and layout yes, blob functions and status-code returns no.)
- **Don't fabricate.** An unknown becomes a `⚠` in your report or a question back to the orchestrator, never an invented value, interface, or "sensible default" the plan didn't authorize.

## Report format

End with a compact, structured report the orchestrator can act on without reading your diff:

- **Task:** `TASK-###` — one line on what you built.
- **Files changed:** the paths you touched (must be a subset of your brief's lane).
- **Interface produced:** the actual signatures/contract you delivered — verbatim, so dependent tasks can build against it.
- **Verify:** the command you ran and its result (green / red + the relevant output). Not "tests pass" — the evidence.
- **Quality:** the `uncle-bob-clean-code` self-review outcome — passes clean, or what you refactored (bloat removed, abstraction collapsed, pattern justified). Not "looks good" — the review result.
- **Deviations / ⚠:** anything you assumed, couldn't verify, or that differs from the brief. Empty is a fine answer; a hidden surprise is not.

## Red flags — stop if you catch yourself thinking…

| Rationalization | Reality |
|---|---|
| "I'll just fix this neighboring file while I'm here." | That file is another worker's lane. Report it; don't touch it. You'll clobber a parallel wave. |
| "I'm confident it's right — I'll commit it." | You never commit. The orchestrator verifies independently and commits. That's the whole safety model. |
| "The code looks correct; I'll report done without running the verify step." | Unrun tests are not evidence. Run it, paste the result, then report. |
| "The brief didn't specify this interface, but this shape seems reasonable." | Inventing an interface breaks the tasks that depend on the promised one. Flag `⚠` and ask; don't guess. |
| "It's a small task, I don't need the clean-code discipline." | Small code is read most. Follow `uncle-bob-clean-code` — the quick version IS the clean version. |
| "Tests are green — done." | Green ≠ good. Run uncle-bob's passes over your diff; verbose or over-abstracted code that passes is still a defect. |
| "Can't reach the real service, but it basically works — I'll say done." | Say code-complete + tested-with-fakes + runbook. Never imply prod-verified. |
| "I'll build the UI freehand, faster than wiring up Impeccable." | UI is built with Impeccable against the style guide, per the plan's global constraint. Freehand UI is drift. |
| "Test's red — let me try a few things and see what turns it green." | Guessing buys a green bar you can't explain. Reproduce → one hypothesis → root cause → minimal fix. |
| "Still red after a dozen edits — one more should do it." | You hit your ceiling. Stop and escalate with what you ruled out. Thrashing buries the real bug. |
| "The reviewer said fix it, so I'll fix it." | Verify the finding first — reproduce it. Unverified agreement is how a bad fix ships. |
| "The reviewer's probably wrong, I'll ignore the notes." | Equally an abdication. Reproduce each finding; act on the real ones, refute the rest with evidence. |

---

*The implementation end of the pipeline: **`requirements-driven-planning`** (the plan) → **`model-routed-delivery`** (routes & dispatches this task to you, verifies and commits your result) → **`clean-implementation`** (this skill — how you build the one task), which **composes `uncle-bob-clean-code`** as its code-quality doctrine.*

*The debug loop, receive-review discipline, and verify-first stance are condensed from [obra/superpowers](https://github.com/obra/superpowers) (`systematic-debugging`, `receiving-code-review`, `test-driven-development`, `verification-before-completion`), scoped to a single dispatched worker.*
