# Orchestrator: deliver a multi-task plan

Announce: **"Using implementation as orchestrator: rate & route → dispatch full waves → verify → review by risk → commit → loop."**

**Core principle: you run a fleet; you don't type code.** Two roles, kept separate:

- **Planner**: decomposes the work into a task DAG; each task gets a difficulty and a model tier.
- **Orchestrator** (this session, on whatever model the user started it with): dispatches, verifies, reviews the risky tasks, commits, keeps the ledger, re-plans. Judgment and verification are the load-bearing work, so the strongest model sits here.

How a worker builds one task is [worker.md](worker.md); every dispatched worker follows it. This file owns routing, waves, verification, commits, and the ledger.

## Your context is the budget

Every turn re-sends your whole context. Your context size times your turn count is the largest cost of a delivery run: in a measured 200-agent run the orchestrator was about half the total, at a typical context of 400k tokens across 3,700 turns. A turn at 40k costs a tenth of one at 400k. So:

- **One session per milestone.** At the end of the milestone gate, write into `STATUS.md` everything the next milestone needs (the plan path, the next wave, open follow-ups, decisions, incidents) and end the session. The next milestone starts in a fresh session from `STATUS.md` and the plan. Past about 200k tokens mid-milestone, do the same at the next wave boundary.
- **Delegate looking.** You don't grep, `cat`, or read source, logs, diffs, or findings to work something out. Ask a small-tier `Explore` agent the question; it answers in a few lines.
- **Reports on disk, verdicts in context.** Workers and reviewers write their full report to `.delivery/<id>.md` (add `.delivery/` to `.git/info/exclude` once) and return one line: id, status, verify result, report path. Open a report only when its line says red, findings, `⚠`, or notes.
- **Filter command output.** Run gates so only failures and the summary come back (`2>&1 | tail -n 40`, or the runner's quiet or failures-only flag). Full logs and screenshots stay with the agent that needs them.
- **Batch.** One shell call per check, not one per step.

## Phase 0: clarify

Ask the questions whose answers change the plan: fail modes, tenancy, scope boundaries, environment ceilings, decisions that fork the architecture. Record the answers. If `planning` has run, its spec and routed plan are the input.

**Ask before using Fable.** Fable costs about three times Opus per token, so the user decides, once, before the plan is written. Ask with the choices below and record the answer in the plan header and `STATUS.md`; it holds for the whole run, including later sessions.

| Answer | Top tier means |
|---|---|
| No Fable (the default when the user doesn't answer or can't be asked) | Opus for everything rated Hard, including `observe` tasks and their reviewers |
| Fable for `observe` only | Fable for `observe` tasks and their per-task reviewers; Opus for other Hard work |
| Fable for all Hard | Fable wherever the routing table says top tier |

Never dispatch a Fable agent without a recorded yes. An escalation under step 7 that would reach Fable without one stops and asks.

**Check the review stamp** before planning on a repo that already has code: run `clean-code-review`'s `review-stamp.sh status`. `stale` means its full review of the whole codebase runs first; the blockers and should-fix findings become tasks in the plan, so new work isn't built on unreviewed code. `fresh`, or a repo with no code yet: carry on.

## Phase 1: plan

Write `IMPLEMENTATION.md` (or `docs/plans/<date>-<name>.md`):

- **Header**: one-sentence goal; 2–3 sentence architecture; stack and global constraints copied verbatim from the spec; the static gate command; milestones M0…Mn, each with an exit criterion.
- **Static gate**: one command that runs the format check, linter, type-check, and a complexity limit. Tools catch mechanical quality problems for free; review tokens go to what tools can't see. If the repo has no such command, creating it is an M0 task.
- **Test gates**: the coverage command with its 90% fail-under threshold, the Compose file that starts real backing services for tests, and the e2e command with a driver that fits the surface (Playwright for browser UI, HTTP for an API, the built binary for a CLI; no Playwright without a browser UI). The Compose file and e2e harness are an M0 task; each e2e scenario is its own task.
- **Per task**: stable id; exact file paths (create / modify / test); the interface it produces, signatures written down; its verify command (the task's tests plus the static gate); difficulty; tier; `observe` and `isolate` flags.
- A task is the smallest unit with its own verify cycle that a reviewer could accept or reject alone. Fold setup into the deliverable task.
- Tasks in one wave touch non-overlapping files. Design the seams so parallel workers never share a file.
- **Simplicity** (the four rules in `uncle-bob-clean-code`). YAGNI: every task traces to a stated requirement; no task builds for a future one. KISS: the plan takes the simplest architecture that meets the requirements. DRY: a shared rule or type is one task's interface that others consume, not something several tasks each write. Convention over configuration: the stack's standard layout, naming, and tooling; a deviation is an `ADR`.
- No "TBD", no "similar to task N". A worker can't recover from an undefined detail; it guesses wrong.
- A "reduce burden" refactor is a valid task (verify: tests green and the target smell gone), scheduled as its own task and commit per `uncle-bob-clean-code`'s `refactoring.md`.

## Phase 2: rate and route

Rate on the **hardest aspect**, not the average.

| Difficulty | Signal | Tier | Today |
|---|---|---|---|
| Easy | mechanical, single-file, pattern-following, reversible | small | Haiku |
| Medium | multi-file, some design judgment, integrates 2–3 components | mid | Opus |
| Hard | security / money / auth / data-integrity / tenancy; concurrency; novel algorithm; many tasks depend on it; high blast radius | top | Opus, or Fable where the user approved it in Phase 0 |

- Use unversioned family names so the mapping doesn't rot; pin a version only to reproduce a run. Sonnet is parked until its effective cost drops below Opus.
- Security / money / auth / data-integrity is **Hard regardless of size**.
- **`observe`** marks the true spine only: key storage, credential or token minting, authn/authz decisions, money movement, tenancy isolation. "Hard" or "auth-adjacent" does not qualify. Expect a small minority of tasks; if a third or more are flagged the flag is diluted, so re-rate. Each flag costs a 30–60 min review plus a fix pass on the critical path.
- The same blast-radius judgment sets **`isolate`** (own worktree at dispatch). Decide once, record both.

## Phase 3: the wave loop

Repeat until the ledger is all green.

1. **Pick the whole wave.** Every ready task whose files are disjoint, usually 6–10. Disjointness was settled in the plan, so don't throttle to 3–5. Hold a task back only if a dependency's interface isn't verified yet or its files overlap.
2. **Dispatch all in one message.** Each brief carries: its files, the interface to produce, the exact verify command, the global constraints verbatim, "use the `implementation` skill as the worker (its `worker.md`)", **never `git commit`**, touch only your files (never `CLAUDE.md`, `AGENTS.md`, `STATUS.md`, or the plan; notes for those go in the report), and the report path `.delivery/<task-id>.md` with the one-line return. Use `general-purpose` with a `model:` override; `isolate` tasks get `isolation: "worktree"`.
   - **Bundle Easy tasks.** Ready Easy tasks in the same package or following the same pattern go to one small-tier worker in one brief (up to about five), built and reported per task. Each is still verified and committed as its own task; if one fails, only that one escalates.
3. **Verify the wave once.** When the wave's workers have reported, run the full suite with its coverage threshold and the static gate once over the tree, against the Compose-started backing services. Green verifies every task in the wave; don't rerun each task's command. Red: run the verify commands of the tasks touching the failing packages to find the culprit, and send that task back to its worker. Coverage under 90% is red: the workers' per-lane figures name the task to send back. The e2e suite is slower, so it runs at the milestone gate, plus the single scenario an e2e task adds.
4. **Review by risk.** Every task gets a `git diff --stat` check from you: changes stay in the task's lane and the size fits the task. Beyond that:

   | Task | Review |
   |---|---|
   | Easy | None. The wave gate and the worker's self-review cover it. |
   | Medium | You skim the diff for what tools miss: hardcoded config, the four simplicity rules (a needless layer, a speculative abstraction or setting, duplicated knowledge, a custom mechanism where the framework has a convention), and for service tasks the Twelve-Factor list in [worker.md](worker.md). |
   | Other Hard | Per wave: one mid-tier reviewer agent over the wave's combined Hard diff. |
   | `observe` | Per task: a fresh top-tier reviewer agent. |

   - A reviewer agent gets the task briefs and file paths and follows `clean-code-review` in scoped mode: those files only, independent of the worker's self-review, trying to refute the work.
   - It writes that skill's report to `.delivery/review-<wave or task id>.md` and returns one line per task: clean, or its finding counts. Don't read Hard diffs yourself; every diff in your context is paid for again on each later turn.
   - Dispatch reviewers in parallel, in one message.
   - Green but bloated, over-abstracted, or hardcoding config is a defect: send it back to the worker to refactor, once. If it comes back still not clean, go to step 7.
   - Confirmed findings go back to the worker under [worker.md](worker.md)'s receive-review rules, pointing at the review file. A reviewer's suggested patch is a claim to adjudicate, not a diff to apply.
   - **Fixes stay at the task's tier.** Send findings to the worker that built the task (continue it with `SendMessage` while it's alive; it already holds the context). A fresh fix worker gets the task's original tier. The top tier fixes only `observe` tasks, or a task escalated under step 7.
   - **One review round.** Review, one fix pass, then a re-review on the small or mid tier limited to the findings and the lines the fix changed (`clean-code-review`'s re-review). Still failing after that: step 7. Never a third round.
5. **Pipeline the reviews.** Once a wave is verified (step 3), dispatch the next wave together with this wave's reviewers; reviews run alongside it. Reviews gate commits, not dispatch. A dependent task may build on a verified-but-uncommitted interface. If a review changes that interface, re-dispatch the uncommitted dependents with the new interface; a dependent already committed gets a follow-up task.
6. **Commit** (orchestrator only): one commit per finished task, staging only that task's paths (never `-A`; other workers share the tree). Update the ledger.
7. **Escalate, then re-plan.** A task that ends red, or green but unable to reach the quality bar after one refactor pass: never re-dispatch the same brief at the same tier. Bump the tier when the brief was sound and the worker couldn't do it; split the task when it was too big to verify in one piece; fix the plan when the interface itself was wrong. Re-plan when a task reveals new work.

## Phase 4: milestone gate

Before declaring a milestone done: `/simplify` over the accumulated diff (dedupe, dead code, collapse parallel solutions to the same concern), then review with `clean-code-review`. Run its `review-stamp.sh status` first: `fresh` means a scoped review of the milestone's accumulated diff; `stale` (14 days or 50 commits since the last full review, or none recorded in `AGENTS.md`) means its full review of the whole codebase, which rewrites the stamp. Fix what's real, then run the full e2e suite on a fresh Compose stack along with the coverage run. Both green, note what's deferred and why, then push. Then update `STATUS.md` for the next milestone and end the session.

## Iron rules

- **Disjoint paths, one worker per file.** Symlinked or aliased directories are the same file. Serialize or re-seam.
- **`isolate` tasks run in their own worktree.** Disjoint paths are a promise a stray worker can break; a worktree makes collision impossible. A worktree costs setup and disk, which is why isolation is a flag rather than the default.
- **Only the orchestrator commits.** Say it in every brief.
- **Only the orchestrator writes shared files**: `CLAUDE.md`, `AGENTS.md`, `STATUS.md`, the plan, the root `README`, and any doc no task owns. Workers and reviewers run in parallel and overwrite each other there, so they report notes instead. After each wave, apply the wave's **Notes for shared docs** yourself, one file at a time, merging duplicates and dropping what the file already says. A doc that a task must update (requirements docs, user docs, a package `README`) is listed in exactly one task's lane, like any other file.
- **`general-purpose` + model override, never a fork.** A fork inherits your commit authorization.
- **Verify before committing.** A worker's "tests pass" is not evidence; the green wave run is.
- **`STATUS.md` is the ledger**: active wave, done tasks, follow-ups, incidents, decisions. Update it every wave; it's how the next context window resumes.
- **Zombie check.** A worker can die silently with no output. When nothing has changed on disk for a while, check each in-flight task's files. A task that wrote nothing never ran, so re-dispatching the same brief is safe (the escalation rule is for tasks that ran and failed). A task that wrote partial output is treated as failed: escalate per step 7.
- **Push once per milestone**, not per task. Each push burns CI.
- **Global constraints exist before dispatch.** If the plan builds a deployable service and lacks the Twelve-Factor constraint, add it. If it lacks the test gates (90% coverage, Compose-backed services, surface-appropriate e2e), add them. Fail-mode per component class must be in the plan before dispatch: fail-closed for spend, auth, governance, budgets, safety; fail-open for soft quotas and rate limits.

## Red flags

| Thought | Reality |
|---|---|
| "I'll write this one myself, it's quick." | Route it. Your job is judgment and verification. |
| "Rerun every task's verify command to be sure." | One full run per wave. Per-task commands are for bisecting a red run. |
| "Read every diff to be safe." | Stat all, skim Medium, delegate Hard. Diffs in your context cost on every later turn. |
| "One worker per Easy task." | Bundle Easy tasks that share a package or pattern. Cold starts cost more than the change. |
| "Adjacent files, probably fine." | Disjoint or serialize. |
| "Hard but small; send it to the mid tier." | Route on the hardest aspect. |
| "Fork myself for speed." | Forks commit. |
| "Have each worker record its learnings in `CLAUDE.md`." | Parallel writers clobber each other. Workers report notes; you write the file. |
| "This task changes behavior, the docs will get updated somewhere." | Put the doc file in that task's lane, or it's nobody's. |
| "Push after each task to be safe." | Git holds it locally. Push per milestone. |
| "Dispatch 3–5 to be safe." | The plan made the wave disjoint. Dispatch all of it. |
| "Flag it `observe`, better safe than sorry." | Each flag is an hour on the critical path. True spine only. |
| "Review each task separately." | Only `observe` tasks. Other Hard tasks share one wave review; Medium gets your skim; Easy gets the gate. |
| "Wait for the reviews before the next wave." | Reviews gate commits, not dispatch. |
| "Coverage is 87%, close enough." | Under 90% is red. Send the short lane back. |
| "Run the e2e suite after every wave." | Milestone gate. Per wave is the full suite with coverage. |
| "The stamp is stale, but the milestone diff is small; review just the diff." | Stale means the whole codebase. That's what the stamp is for. |
| "Huge diff, skip the gate." | Big diffs hide regressions. Run it. |
| "Tests pass; commit." | Run the wave gate yourself, then review at the task's tier. Green isn't clean. |
| "Re-dispatch the same brief." | Same brief, same tier, same result. Escalate. |
| "Apply the reviewer's patch." | Adjudicate the claim; route it through the worker. |
| "Disjoint paths are enough for this risky wave." | High blast radius → `isolate`. |
| "Quick grep to check." / "Let me read that file." | Everything you read is re-sent on every later turn. Ask an `Explore` agent. |
| "Paste the full report back; I'll want the detail." | One line back, the report on disk. Open it only when the line says so. |
| "Stay in this session; it already has the context." | `STATUS.md` has what the next milestone needs. Fresh session per milestone. |
| "One more review round to be sure." | One review, one fix, one narrow re-check. Then escalate. |
| "This one is really hard; Fable just this once." | Fable needs the user's recorded yes from Phase 0. No record: Opus, or stop and ask. |
| "Send the fix to the top tier so it's done right." | Fix at the task's tier. The top tier is for `observe` tasks and escalations. |

