# Orchestrator: deliver a multi-task plan

Announce: **"Using implementation as orchestrator: plan feature slices → dispatch full waves → verify → commit → review each finished feature once."**

**Core principle: you run a fleet; you don't type code.** Every task is routed, including the quick ones; your work is judgment and verification. Two roles, kept separate:

- **Planner**: decomposes the work into a task DAG; each task gets a difficulty and a model tier.
- **Orchestrator** (this session, on whatever model the user started it with): dispatches, verifies, has each finished feature reviewed, commits, keeps the ledger, re-plans. Judgment and verification are the load-bearing work, so the strongest model sits here.

How a worker builds one task is [worker.md](worker.md); every dispatched worker follows it. This file owns routing, waves, verification, commits, and the ledger.

## Your context is the budget

Every turn re-sends your whole context. Your context size times your turn count is the largest cost of a delivery run: in a measured 200-agent run the orchestrator was about half the total, at a typical context of 400k tokens across 3,700 turns. A turn at 40k costs a tenth of one at 400k. So:

- **One session per milestone.** At the end of the milestone gate, write into `STATUS.md` everything the next milestone needs (the plan path, the next wave, open follow-ups, decisions, incidents) and end the session. The next milestone starts in a fresh session from `STATUS.md` and the plan. Past about 200k tokens mid-milestone, do the same at the next wave boundary.
- **Delegate looking.** You don't grep, `cat`, or read source, logs, diffs, or findings to work something out. Ask a small-tier `Explore` agent the question; it answers in a few lines.
- **Reports on disk, verdicts in context.** Workers and reviewers write their full report to `.delivery/<id>.md` (add `.delivery/` to `.git/info/exclude` once) and return one line: id, status, verify result, report path. Open a report only when its line says red, findings, `⚠`, or notes.
- **Filter command output.** Run gates so only failures and the summary come back (`2>&1 | tail -n 40`, or the runner's quiet or failures-only flag). Full logs and screenshots stay with the agent that needs them.
- **Batch.** One shell call per check, not one per step.

## Phase 0: clarify

Ask the questions whose answers change the plan: fail modes, tenancy, scope boundaries, environment ceilings, decisions that fork the architecture. Work the open decisions as a tree, in **rounds**. A round is every question you can ask now without guessing at an answer you haven't heard. Number each question, give your recommended answer, and word it so "yes" accepts the recommendation; then wait. Each answer unblocks the next round. Facts are yours to find (send an `Explore` agent to the code, the docs, the environment); only decisions go to the user. Done when no decision is left assumed. Record the answers. If `chadgrant:planning` has run, its spec and routed plan are the input.

**Ask before using Fable.** Fable costs about three times Opus per token, so the user decides, once, before the plan is written. Ask with the choices below and record the answer in the plan header and `STATUS.md`; it holds for the whole run, including later sessions.

| Answer | Top tier means |
|---|---|
| No Fable (the default when the user doesn't answer or can't be asked) | Opus for everything rated Hard, including `observe` tasks and their reviewers |
| Fable for `observe` only | Fable for `observe` tasks and their security reviewer; Opus for other Hard work |
| Fable for all Hard | Fable wherever the routing table says top tier |

Never dispatch a Fable agent without a recorded yes. An escalation under step 6 that would reach Fable without one stops and asks.

**Check the review stamp** on a repo that already has code: run `chadgrant:code-review`'s `review-stamp.sh status`. On `stale`, tell the user once, in one line, and carry on: "Full code review is stale (<the script's reason>). Run `chadgrant:code-review` on the whole codebase when you want it." A full review is exhaustive and its fixes are a project of their own, so it runs only when the user asks for it. Say it once here and once in the milestone summary, never per wave.

## Phase 1: plan

Write `IMPLEMENTATION.md` (or `docs/plans/<date>-<name>.md`):

- **Header**: one-sentence goal; 2–3 sentence architecture; stack and global constraints copied verbatim from the spec; the static gate command; milestones M0…Mn, each with an exit criterion.
- **Static gate**: one command that runs the format check, linter, type-check, and a complexity limit. Tools catch mechanical quality problems for free; review tokens go to what tools can't see. If the repo has no such command, creating it is an M0 task.
- **Test gates**: the coverage command with its 90% fail-under threshold, the Compose file that starts real backing services for tests, and the e2e command with a driver that fits the surface (Playwright for browser UI, HTTP for an API, the built binary for a CLI; no Playwright without a browser UI). The Compose file and e2e harness are an M0 task; each e2e scenario is its own task.
- **Per task**: stable id; the directories or packages it owns; the interface it exposes to other tasks, only where another task calls it; its verify command (the task's tests plus the static gate); difficulty; tier; `observe` and `isolate` flags.
- **A task is a feature slice**: one user-visible capability (one or a few `REQ`s) built end to end through every layer it needs (schema, logic, API, UI, tests) by one worker, and demoable on its own. Size it to what one agent can build and verify in one session, typically a few hundred to about 1,500 changed lines. A project is usually 5–15 tasks, not 50. Two tasks that would each change under about 100 lines, or that share files, are one task. Never split by layer (a model task, then a repository task, then a handler task); that multiplies briefs, interfaces, and verify cycles for no gain.
- **A milestone is a big feature**: a set of slices that together deliver something a user would notice. It ends at the milestone gate, which is where review happens.
- Tasks in one wave touch non-overlapping files. Design the seams so parallel workers never share a file.
- **Simplicity** (the four rules in `chadgrant:clean-code`). YAGNI: every task traces to a stated requirement; no task builds for a future one. KISS: the plan takes the simplest architecture that meets the requirements. DRY: a shared rule or type is one task's interface that others consume, not something several tasks each write. Convention over configuration: the stack's standard layout, naming, and tooling; a deviation is an `ADR`.
- No "TBD", no "similar to task N". A worker can't recover from an undefined detail; it guesses wrong.
- A "reduce burden" refactor is a valid task (verify: tests green and the target smell gone), scheduled as its own task and commit per `chadgrant:clean-code`'s `refactoring.md`.

## Phase 2: rate and route

Rate on the **hardest aspect**, not the average.

| Difficulty | Signal | Tier | Today |
|---|---|---|---|
| Easy | mechanical, single-file, pattern-following, reversible | small | Haiku |
| Medium | multi-file, some design judgment, integrates 2–3 components | mid | Opus |
| Hard | security / money / auth / data-integrity / tenancy; concurrency; novel algorithm; many tasks depend on it; high blast radius | top | Opus, or Fable where the user approved it in Phase 0 |

- Use unversioned family names so the mapping doesn't rot; pin a version only to reproduce a run. Sonnet is parked until its effective cost drops below Opus.
- Security / money / auth / data-integrity is **Hard regardless of size**.
- **`observe`** marks the true spine only: key storage, credential or token minting, authn/authz decisions, money movement, tenancy isolation. "Hard" or "auth-adjacent" does not qualify. It adds a security reviewer at the milestone gate; it does not add a review per task.
- The same blast-radius judgment sets **`isolate`** (own worktree at dispatch). Decide once, record both.

## Phase 3: the wave loop

Repeat until the ledger is all green.

1. **Pick the whole wave.** Every ready task whose files are disjoint. Hold a task back only if a dependency's interface isn't built yet or its files overlap.
2. **Dispatch all in one message.** Each brief carries: the task's goal and the `REQ`s it satisfies, the directories it owns, the interfaces it exposes or consumes, the exact verify command, a pointer to the plan's global constraints (the file and heading; the worker reads them there, you don't restate them), "use the `chadgrant:implementation` skill as the worker (its `worker.md`)", **never `git commit`**, touch only your files (never `CLAUDE.md`, `AGENTS.md`, `STATUS.md`, or the plan; notes for those go in the report), the path to `GLOSSARY.md` when the repo has one, and the report path `.delivery/<task-id>.md` with the one-line return. Use `general-purpose` with a `model:` override; `isolate` tasks get `isolation: "worktree"`.
3. **Verify the wave once.** When the wave's workers have reported, run the full suite with its coverage threshold and the static gate once over the tree, against the Compose-started backing services. Green verifies every task in the wave. Red: run the verify commands of the tasks touching the failing packages to find the culprit, and send that task back to its worker. Coverage under 90% is red: the workers' per-lane figures name the task to send back. The e2e suite runs at the milestone gate, plus the scenarios a task adds.
4. **Check the lanes.** `git diff --stat` per task: changes stay in the task's directories and the size fits the task. That is the whole per-wave check. Code review waits for the milestone gate, when there is a whole feature to review.
5. **Commit** (orchestrator only): one commit per green task, staging only that task's paths (never `-A`; other workers share the tree). Update the ledger and dispatch the next wave.
6. **Escalate, then re-plan.** A task that ends red: never re-dispatch the same brief at the same tier. Bump the tier when the brief was sound and the worker couldn't do it; split the task when it was too big to verify in one piece; fix the plan when the interface itself was wrong. Re-plan when a task reveals new work.

## Phase 4: milestone gate

Before declaring a milestone done: `/simplify` over the accumulated diff (dedupe, dead code, collapse parallel solutions to the same concern), then review the feature.

**Review the feature, once.** One `chadgrant:code-review` in scoped mode over the milestone's accumulated diff (`git diff <milestone start>..HEAD`), on the mid tier, with the milestone's `REQ`s as the spec. When the milestone has `observe` tasks, add one top-tier reviewer for the security lens over those tasks' files. Both write to `.delivery/review-<milestone>.md` and return one line.

- **Fix blockers and should-fix findings; list nits and don't fix them.** Group the findings by owning task and send each group to one worker at the task's tier, all in one message. Fixes run under [worker.md](worker.md)'s receive-review rules.
- **One round.** After the fixes, re-run the wave gate. No second review: a finding still open after the fix pass is escalated under step 6 of the wave loop or recorded as deferred in `STATUS.md`.

Then run the full e2e suite on a fresh Compose stack along with the coverage run. Both green, note what's deferred and why, then push.

**Compact the requirements** when they're due: run `chadgrant:planning`'s compaction (its Path D) on a mid-tier agent, committed on its own so the diff can be read. Due means any `Recent changes` entry that this milestone implemented or that is more than 14 days old.

**Nag, don't review.** Run `review-stamp.sh status` again; on `stale`, end your milestone summary with the one-line nag from Phase 0.

**Retro.** Before ending the session, have a mid-tier agent read this milestone's `.delivery/` reports and review files and return at most ten improvements to the environment, most costly problem first. You apply them or schedule them as tasks:

| What kept happening | The fix |
|---|---|
| The same mechanical finding in several reviews (a banned call, an import shape, a naming or file-location rule) | A lint rule or a check in the static gate. Tools enforce it from then on and reviewers stop spending on it. |
| The same judgement finding in several reviews | One line under conventions in `AGENTS.md`, or in the plan's global constraints |
| Workers asking, guessing, or flagging `⚠` about the same gap | Fix the plan or the brief wording |
| Workers hunting for the same file, command, or fact | A pointer in `AGENTS.md` |
| A tool call that returned far more than was needed | A filtered command or script, named in `AGENTS.md` |
| A line in `AGENTS.md` or `CLAUDE.md` no run needed | Delete it |

Then update `STATUS.md` for the next milestone and end the session.

## Iron rules

- **Disjoint paths, one worker per file.** Symlinked or aliased directories are the same file. Serialize or re-seam.
- **`isolate` tasks run in their own worktree.** Disjoint paths are a promise a stray worker can break; a worktree makes collision impossible. A worktree costs setup and disk, which is why isolation is a flag rather than the default.
- **Only the orchestrator commits.** Say it in every brief.
- **Only the orchestrator writes shared files**: `CLAUDE.md`, `AGENTS.md`, `STATUS.md`, the plan, the root `README`, and any doc no task owns. Workers and reviewers run in parallel and overwrite each other there, so they report notes instead. After each wave, apply the wave's **Notes for shared docs** yourself, one file at a time, merging duplicates and dropping what the file already says. A doc that a task must update (requirements docs, user docs, a package `README`) is listed in exactly one task's lane, like any other file.
- **`general-purpose` + model override, never a fork.** A fork inherits your commit authorization.
- **Verify before committing.** A worker's "tests pass" is not evidence; the green wave run is, and the bigger the diff the more it matters.
- **`STATUS.md` is the ledger**: active wave, done tasks, follow-ups, incidents, decisions. Update it every wave; it's how the next context window resumes.
- **Zombie check.** A worker can die silently with no output. When nothing has changed on disk for a while, check each in-flight task's files. A task that wrote nothing never ran, so re-dispatching the same brief is safe (the escalation rule is for tasks that ran and failed). A task that wrote partial output is treated as failed: escalate per step 6.
- **Push once per milestone**, not per task. Each push burns CI.
- **Global constraints exist before dispatch.** If the plan builds a deployable service and lacks the Twelve-Factor constraint, add it. If it lacks the test gates (90% coverage, Compose-backed services, surface-appropriate e2e), add them. Fail-mode per component class must be in the plan before dispatch: fail-closed for spend, auth, governance, budgets, safety; fail-open for soft quotas and rate limits.
