---
name: model-routed-delivery
description: Use when delivering a multi-task build (a project, milestone, or migration) mostly autonomously from an existing spec or routed plan, or when running waves of subagents whose results must be verified and committed. Triggers: "build the plan", "run the waves", "orchestrate this", "execute IMPLEMENTATION.md".
---

# Model-routed delivery

Announce: **"Using model-routed-delivery: rate & route → dispatch full waves → verify → review by risk → commit → loop."**

**Core principle: you run a fleet; you don't type code.** Two roles, kept separate:

- **Planner**: decomposes the work into a task DAG; each task gets a difficulty and a model tier.
- **Orchestrator** (this session, on the top tier): dispatches, verifies, reviews the risky tasks, commits, keeps the ledger, re-plans. Judgment and verification are the load-bearing work, so the strongest model sits here.

How a worker builds one task is `clean-implementation`'s job; every dispatched worker follows it. This skill owns routing, waves, verification, commits, and the ledger.

## Phase 0: clarify

Ask the questions whose answers change the plan: fail modes, tenancy, scope boundaries, environment ceilings, decisions that fork the architecture. Record the answers. If `requirements-driven-planning` has run, its spec and routed plan are the input.

## Phase 1: plan

Write `IMPLEMENTATION.md` (or `docs/plans/<date>-<name>.md`):

- **Header**: one-sentence goal; 2–3 sentence architecture; stack and global constraints copied verbatim from the spec; milestones M0…Mn, each with an exit criterion.
- **Per task**: stable id; exact file paths (create / modify / test); the interface it produces, signatures written down; its verify command; difficulty; tier; `observe` and `isolate` flags.
- A task is the smallest unit with its own verify cycle that a reviewer could accept or reject alone. Fold setup into the deliverable task.
- Tasks in one wave touch non-overlapping files. Design the seams so parallel workers never share a file.
- No "TBD", no "similar to task N". A worker can't recover from an undefined detail; it guesses wrong.
- A "reduce burden" refactor is a valid task (verify: tests green and the target smell gone), scheduled as its own task and commit per `refactoring`.

## Phase 2: rate and route

Rate on the **hardest aspect**, not the average.

| Difficulty | Signal | Tier | Today |
|---|---|---|---|
| Easy | mechanical, single-file, pattern-following, reversible | small | Haiku |
| Medium | multi-file, some design judgment, integrates 2–3 components | mid | Opus |
| Hard | security / money / auth / data-integrity / tenancy; concurrency; novel algorithm; many tasks depend on it; high blast radius | top | Fable |

- Use unversioned family names so the mapping doesn't rot; pin a version only to reproduce a run. Sonnet is parked until its effective cost drops below Opus.
- Security / money / auth / data-integrity is **Hard regardless of size**.
- **`observe`** marks the true spine only: key storage, credential or token minting, authn/authz decisions, money movement, tenancy isolation. "Hard" or "auth-adjacent" does not qualify. Expect a small minority of tasks; if a third or more are flagged the flag is diluted, so re-rate. Each flag costs a 30–60 min review plus a fix pass on the critical path.
- The same blast-radius judgment sets **`isolate`** (own worktree at dispatch). Decide once, record both.

## Phase 3: the wave loop

Repeat until the ledger is all green.

1. **Pick the whole wave.** Every ready task whose files are disjoint, usually 6–10. Disjointness was settled in the plan, so don't throttle to 3–5. Hold a task back only if a dependency's interface isn't verified yet or its files overlap.
2. **Dispatch all in one message.** Each brief carries: its files, the interface to produce, the exact verify command, the global constraints verbatim, "build it by following `clean-implementation`", **never `git commit`**, and touch only your files. Use `general-purpose` with a `model:` override; `isolate` tasks get `isolation: "worktree"`.
3. **Verify each result yourself.** Run its verify command scoped to the touched packages (the tree may be transiently red from other workers); run the full suite once the wave lands. Then run `uncle-bob-clean-code`'s three review passes over the diff, independent of the worker's self-review; service tasks are also checked against the Twelve-Factor list in `clean-implementation`. Green but bloated, over-abstracted, or hardcoding config is a defect: send it back to the worker to refactor, once. If it comes back still not clean, go to step 7.
4. **Review by risk.**

   | Task | Adversarial review |
   |---|---|
   | `observe` | Per task: a fresh agent told to refute it, name the breaking inputs, prove the invariant holds. |
   | Other Hard | Per wave: one review over the wave's combined Hard diff. |
   | Medium / Easy | None. Step 3 catches what matters. |

   Confirmed findings go back to the worker under `clean-implementation`'s receive-review rules. A reviewer's suggested patch is a claim to adjudicate, not a diff to apply.
5. **Pipeline the reviews.** Once a wave is verified (step 3), dispatch the next wave; reviews run alongside it. Reviews gate commits, not dispatch. A dependent task may build on a verified-but-uncommitted interface. If a review changes that interface, re-dispatch the uncommitted dependents with the new interface; a dependent already committed gets a follow-up task.
6. **Commit** (orchestrator only): one commit per finished task, staging only that task's paths (never `-A`; other workers share the tree). Update the ledger.
7. **Escalate, then re-plan.** A task that ends red, or green but unable to reach the quality bar after one refactor pass: never re-dispatch the same brief at the same tier. Bump the tier when the brief was sound and the worker couldn't do it; split the task when it was too big to verify in one piece; fix the plan when the interface itself was wrong. Re-plan when a task reveals new work.

## Phase 4: milestone gate

Before declaring a milestone done: `/simplify` over the accumulated diff (dedupe, dead code, collapse parallel solutions to the same concern), then `/code-review`. Fix what's real, note what's deferred and why, then push.

## Iron rules

- **Disjoint paths, one worker per file.** Symlinked or aliased directories are the same file. Serialize or re-seam.
- **`isolate` tasks run in their own worktree.** Disjoint paths are a promise a stray worker can break; a worktree makes collision impossible. A worktree costs setup and disk, which is why isolation is a flag rather than the default.
- **Only the orchestrator commits.** Say it in every brief.
- **`general-purpose` + model override, never a fork.** A fork inherits your commit authorization.
- **Verify before committing.** A worker's "tests pass" is not evidence.
- **`STATUS.md` is the ledger**: active wave, done tasks, follow-ups, incidents, decisions. Update it every wave; it's how the next context window resumes.
- **Zombie check.** A worker can die silently with no output. When nothing has changed on disk for a while, check each in-flight task's files. A task that wrote nothing never ran, so re-dispatching the same brief is safe (the escalation rule is for tasks that ran and failed). A task that wrote partial output is treated as failed: escalate per step 7.
- **Push once per milestone**, not per task. Each push burns CI.
- **Global constraints exist before dispatch.** If the plan builds a deployable service and lacks the Twelve-Factor constraint, add it. Fail-mode per component class must be in the plan before dispatch: fail-closed for spend, auth, governance, budgets, safety; fail-open for soft quotas and rate limits.
- **Honest environment ceiling.** Without real cloud, certs, or live services, "done" means code-complete + tested with fakes + a runbook. Never imply production-verified.

## Red flags

| Thought | Reality |
|---|---|
| "I'll write this one myself, it's quick." | Route it. Your job is judgment and verification. |
| "The worker said tests pass; commit." | Run them yourself. |
| "Adjacent files, probably fine." | Disjoint or serialize. |
| "Hard but small; send it to the mid tier." | Route on the hardest aspect. |
| "Fork myself for speed." | Forks commit. |
| "Push after each task to be safe." | Git holds it locally. Push per milestone. |
| "Dispatch 3–5 to be safe." | The plan made the wave disjoint. Dispatch all of it. |
| "Flag it `observe`, better safe than sorry." | Each flag is an hour on the critical path. True spine only. |
| "Review each task separately." | Only `observe` tasks. Other Hard tasks share one wave review; Medium/Easy get none. |
| "Wait for the reviews before the next wave." | Reviews gate commits, not dispatch. |
| "It builds, ship it." | `observe` tasks are reviewed first. |
| "Huge diff, skip the gate." | Big diffs hide regressions. Run it. |
| "Tests pass; commit." | Green isn't clean. Quality-pass the diff first. |
| "Re-dispatch the same brief." | Same brief, same tier, same result. Escalate. |
| "Apply the reviewer's patch." | Adjudicate the claim; route it through the worker. |
| "Disjoint paths are enough for this risky wave." | High blast radius → `isolate`. |

---

*Middle of the pipeline: `requirements-driven-planning` → **`model-routed-delivery`** → `clean-implementation`. Structure inspired by [obra/superpowers](https://github.com/obra/superpowers).*
