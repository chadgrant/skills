---
name: clean-implementation
description: Use when building a single task from a plan — the worker's operating manual for turning one task brief into verified, clean, committed-ready code. Applies whether you're a Claude Code subagent dispatched by model-routed-delivery or an autonomous "dark factory" node. Understand the task and its interface contract, work verify-first, write the code by following the uncle-bob-clean-code skill, build UI with Impeccable against the style guide, stay in your assigned files, never commit, and report the interface you produced back to the orchestrator. Triggers: "implement TASK-###", "build this task", a dispatched task brief, "you are the worker".
---

# Clean implementation

Announce at the start: **"Using clean-implementation: read the brief → verify-first → write it clean → prove it green → report back."**

**Core principle: your job is one task, done well and proven — not the whole system.** You are a **worker**, not the orchestrator. Someone above you decomposed the work, routed this task to you, and will verify, commit, and integrate your result. Your entire contract is: build exactly the task in your brief, make its verify step pass, and hand back a truthful report. Doing more, touching more, or claiming more is a defect.

This is the **implementation** end of the pipeline (`requirements-driven-planning` → `model-routed-delivery` → **`clean-implementation`**). The layer above owns routing, waves, commits, and the ledger. You own the keystrokes for one unit of work.

## Your input: the task brief

A well-formed brief gives you everything you need. Confirm you have it before typing:

- **Task id + goal** — the one thing this task delivers.
- **Files** — exactly which to create / modify / test. This set is your lane; it is disjoint from every other in-flight worker's lane on purpose.
- **Interface to produce** — the signatures, types, or contract later tasks depend on. This is a promise; match it exactly.
- **Verify step** — the exact build/test command that proves the task done, needing no human interpretation.
- **Difficulty / `observe` flag** — if flagged `observe`, expect an adversarial review of your result; write to survive it.
- **Global constraints** — stack, fail-mode, and (for UI work) the Impeccable + style-guide constraint, copied verbatim from the plan.

**Missing or ambiguous brief?** Don't guess your way past a genuine fork — a wrong assumption here becomes wrong code the orchestrator has to catch and unwind. State the ambiguity in your report and, where you can, proceed on the smallest defensible interpretation and flag it `⚠`. Never invent an interface the plan didn't specify.

## The build loop

1. **Read the task and its interface contract first.** Know what you must produce and what you may depend on before you write a line. Read the files in your lane and the interfaces of the tasks yours depends on — not the whole tree.
2. **Verify-first.** Where the environment allows, write the failing test from the verify step before the implementation (uncle-bob's Three Laws of TDD). The verify step is the target; make it fail for the right reason, then make it pass.
3. **Write the code by following the `uncle-bob-clean-code` skill.** That skill is this skill's code-quality doctrine — small single-purpose functions, intention-revealing names, exceptions over status codes, no flag arguments, SOLID at genuine seams, and its own "don't over-apply" guardrails. Do not restate or second-guess it; invoke it and follow it. The Boy Scout Rule applies to lines you touch — and only those.
4. **UI/site work → build with Impeccable.** If the task has a user-facing surface, build it with the [Impeccable](https://github.com/pbakaus/impeccable) skill against the design system's `TOK-`/`CMP-` from the project's style guide (`design-system/style-guide.md`), per the plan's global constraint. Lo-fi wireframes define layout; the style guide defines visual language; Impeccable is how it gets built.
5. **Prove it green.** Run your task's exact verify step **yourself**. The task is not done until its `TEST-` passes for the right reason. A worker who reports "done" on unrun tests has handed the orchestrator a live grenade.
6. **Report back** (see format below). Your final message is a structured report to the orchestrator, not prose for a human.

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
- **Deviations / ⚠:** anything you assumed, couldn't verify, or that differs from the brief. Empty is a fine answer; a hidden surprise is not.

## Red flags — stop if you catch yourself thinking…

| Rationalization | Reality |
|---|---|
| "I'll just fix this neighboring file while I'm here." | That file is another worker's lane. Report it; don't touch it. You'll clobber a parallel wave. |
| "I'm confident it's right — I'll commit it." | You never commit. The orchestrator verifies independently and commits. That's the whole safety model. |
| "The code looks correct; I'll report done without running the verify step." | Unrun tests are not evidence. Run it, paste the result, then report. |
| "The brief didn't specify this interface, but this shape seems reasonable." | Inventing an interface breaks the tasks that depend on the promised one. Flag `⚠` and ask; don't guess. |
| "It's a small task, I don't need the clean-code discipline." | Small code is read most. Follow `uncle-bob-clean-code` — the quick version IS the clean version. |
| "Can't reach the real service, but it basically works — I'll say done." | Say code-complete + tested-with-fakes + runbook. Never imply prod-verified. |
| "I'll build the UI freehand, faster than wiring up Impeccable." | UI is built with Impeccable against the style guide, per the plan's global constraint. Freehand UI is drift. |

---

*The implementation end of the pipeline: **`requirements-driven-planning`** (the plan) → **`model-routed-delivery`** (routes & dispatches this task to you, verifies and commits your result) → **`clean-implementation`** (this skill — how you build the one task), which **composes `uncle-bob-clean-code`** as its code-quality doctrine.*
