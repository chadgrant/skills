# Orchestrator: deliver a multi-task plan

Announce: **"Using implementation as orchestrator: contracts first → implement them in parallel → verify → commit → review each finished feature once."**

**Core principle: you run a fleet; you don't type code.** Every task is routed, including the quick ones; your work is judgment and verification. Two roles, kept separate:

- **Planner**: decomposes the work into a task DAG; each task gets a difficulty and a model tier.
- **Orchestrator** (this session, on whatever model the user started it with): dispatches, verifies, has each finished feature reviewed, commits, keeps the ledger, re-plans. Judgment and verification are the load-bearing work, so the strongest model sits here.

How a worker builds one task is [worker.md](worker.md); every dispatched worker follows it. This file owns routing, waves, verification, commits, and the ledger.

## Your context is the budget

Every turn re-sends your whole context. Your context size times your turn count is the largest cost of a delivery run: in a measured 200-agent run the orchestrator was about half the total, at a typical context of 400k tokens across 3,700 turns. A turn at 40k costs a tenth of one at 400k. So:

- **One session per milestone.** At the end of the milestone gate, write into `STATUS.md` everything the next milestone needs (the plan path, the next wave, open follow-ups, decisions, incidents) and end the session. The next milestone starts in a fresh session from `STATUS.md` and the plan. Past about 200k tokens mid-milestone, do the same at the next wave boundary.
- **Delegate looking.** You don't grep, `cat`, or read source, logs, diffs, or findings to work something out. Ask a small-tier `Explore` agent the question; it answers in a few lines.
- **Reports on disk, verdicts in context.** Workers and reviewers write their full report to `.delivery/<id>.md` in the main checkout (add `.delivery/` to `.git/info/exclude` once, and give workers its absolute path, since they run in worktrees) and return one line: id, status, verify result, report path. Open a report only when its line says red, findings, `⚠`, or notes.
- **Filter command output.** Run gates so only failures and the summary come back (`2>&1 | tail -n 40`, or the runner's quiet or failures-only flag). Full logs and screenshots stay with the agent that needs them.
- **Batch.** One shell call per check, not one per step.

## The journal

Every run is timed, so slow stages can be found with data instead of guessed at. `J` below means `python3 <this skill's directory>/scripts/journal.py`; it appends to one file per project, `~/.claude/journal/<repo name>.jsonl` (`J path` prints it). Log as you go, one shell call per event; each call costs a few tokens and nothing else.

The plugin's hooks already log every subagent on their own: its wall time, the share of that spent waiting on the model, requests, tokens, model, the API provider (Anthropic, Bedrock, Vertex, or a gateway), and every API failure. You don't log those. Your calls below add what only you know: which task, which wave, and how it turned out. `J report --providers` compares providers' speed and failure rates. Every event also records the skills' version and git commit, so `J report --versions` shows whether a change to these skills made runs faster or cleaner.

| When | Call |
|---|---|
| The run starts, unless the plan header or `STATUS.md` already names an open run | `J begin run <YYYY-MM-DD-slug> fable=<answer> tasks=<count>`, and write the run id into `STATUS.md` |
| A milestone starts / ends | `J begin phase milestone m=<M1>` / `J end phase milestone m=<M1>` |
| A wave is dispatched / verified | `J begin wave <M1-W1> tasks=<n>` / `J end wave <M1-W1> conflicts=<n>` |
| A task is dispatched / its report arrives | `J begin task <TASK-007> tier=<tier> model=<model> difficulty=<d>` / `J end task <TASK-007> outcome=<green\|red\|escalated> attempt=<n> lines=<changed lines> tokens=<if the agent result gives them>` |
| A gate runs | `J begin gate <fast\|full> m=<M1>` / `J end gate <fast\|full> outcome=<green\|red> failures=<n>` |
| A milestone stage runs (`contracts`, `simplify`, `compact`, `retro`) | `J begin phase <stage> m=<M1>` / `J end phase <stage> m=<M1>` |
| The feature review / the fix pass | `J begin review feature m=<M1>` / `J end review feature blockers=<n> should_fix=<n> nits=<n>`; `J begin fix pass m=<M1>` / `J end fix pass tasks=<n>` |
| Something worth knowing later (an escalation and why, a zombie worker, a crash, a slow command) | `J note <one line>` |
| The last milestone ends | `J end run <id>` |

Names stay the same from run to run (`gate full`, `phase simplify`) so `J report --all` can compare runs; the milestone goes in a field. At each milestone summary, include the few lines of `J report` that matter: task count and median, and the longest stages.

## Phase 0: clarify

Ask the questions whose answers change the plan: fail modes, tenancy, scope boundaries, environment ceilings, decisions that fork the architecture. Work the open decisions as a tree, in **rounds**. A round is every question you can ask now without guessing at an answer you haven't heard. Number each question, give your recommended answer, and word it so "yes" accepts the recommendation; then wait. Each answer unblocks the next round. Facts are yours to find (send an `Explore` agent to the code, the docs, the environment); only decisions go to the user. Done when no decision is left assumed. Record the answers. If `chadgrant:planning` has run, its spec and routed plan are the input.

**Ask before using Fable.** Fable costs about three times Opus per token, so the user decides, once, before the plan is written. Ask with the choices below and record the answer in the plan header and `STATUS.md`; it holds for the whole run, including later sessions.

| Answer | Top tier means |
|---|---|
| No Fable (the default when the user doesn't answer or can't be asked) | Opus for everything rated Hard, including `observe` tasks and their reviewers |
| Fable for `observe` only | Fable for `observe` tasks and their security reviewer; Opus for other Hard work |
| Fable for all Hard | Fable wherever the routing table says top tier |

Never dispatch a Fable agent without a recorded yes. An escalation under step 6 that would reach Fable without one stops and asks.

**Write the architecture note** before the first wave on a repo that already has code, unless `AGENTS.md` already has a current one. A mid-tier agent writes an `## Architecture` section of at most about 60 lines: how the pieces are wired (how a screen mounts in each shell, how routes and sub-tabs are registered, where each kind of file lives), the hot files and how to add to them, the test command per package, and how to set up a fresh worktree (installing dependencies). You read it, correct it, and commit it. Every worker reads it first, so no worker spends its first half hour re-learning the same five things. The retro keeps it current.

**Check the review stamp** on a repo that already has code: run `chadgrant:code-review`'s `review-stamp.sh status`. On `stale`, tell the user once, in one line, and carry on: "Full code review is stale (<the script's reason>). Run `chadgrant:code-review` on the whole codebase when you want it." A full review is exhaustive and its fixes are a project of their own, so it runs only when the user asks for it. Say it once here and once in the milestone summary, never per wave.

## Phase 1: plan

Write `IMPLEMENTATION.md` (or `docs/plans/<date>-<name>.md`):

- **Header**: one-sentence goal; 2–3 sentence architecture; stack and global constraints copied verbatim from the spec; the static gate command; `max_parallel`, the most workers running at once (default 4; the user may set another); milestones M0…Mn, each with an exit criterion.
- **Static gate**: one command that runs the format check, linter, type-check, and a complexity limit. Tools catch mechanical quality problems for free; review tokens go to what tools can't see. If the repo has no such command, creating it is an M0 task.
- **Two test gates**, one command each:
  - **Fast gate**: unit and other self-contained tests plus the static gate. No Docker, no database, no network services, so it runs anywhere, in parallel, cheaply. Workers run it in their worktrees; you run it once per wave on the merged tree.
  - **Full gate**: integration tests against real backing services (started with Docker Compose when the project has it), coverage with its 90% fail-under threshold, and the e2e suite with a driver that fits the surface (Playwright for browser UI, HTTP for an API, the built binary for a CLI; no Playwright without a browser UI). Only you run it, once per milestone, before `/simplify` and review. A project without backing services or Compose has a full gate of whatever integration and e2e commands it has.
  - The harness for both is an M0 task; each e2e scenario belongs to the feature that needs it.
- **Per task**: stable id; the `CON`s it implements and the `CON`s it consumes; the hot files it touches; difficulty; tier; `observe` flag. Every task's verify step is the fast gate, which includes its contracts' contract tests.
- **Contracts**: the `CON-###` entries for each milestone (the plan's contract table): every interface, abstract class, protocol, and shared type the milestone's tasks call across each other, each with its final file path, its members, and the behavior its doc comment will state. Writing them is the first task of every milestone (Phase 3).
- **A task implements contracts**: a cohesive group of `CON`s (one module, or one bounded context's part of the feature) built with its tests by one worker. **Size it so the worker's context stays small**: up to about 400 changed lines and one screen, endpoint group, or module. A worker's context grows with everything it reads, and every turn re-sends all of it; in a measured run contexts grew from 24k to 250–330k tokens, model time was 88% of worker time, and a 450-line task still took 28 minutes. Exactly one task implements each contract. Group by cohesion, never by layer of one feature; two tasks that would each change under about 100 lines are one task. The task count follows from the size.
- **Choose the team size.** Parallel workers pay off only when the work splits into independent contracts. A milestone with fewer than three independent implementation tasks, or one tightly coupled piece (a parser, an algorithm, a single state machine), goes to one worker who writes the contracts and builds them in sequence. On small work a single agent beats a team; a plan of one task is a valid plan.
- **A milestone is a big feature**: a set of slices that together deliver something a user would notice. It ends at the milestone gate, which is where review happens.
- **Every task runs in its own git worktree**, so tasks in one wave may touch the same files and you merge them. **Hot files**, the few that every feature edits (route registry, dependency wiring, migration numbering, a shared enum), are set up in M0 to take additions without conflict: one file per route group, timestamped migrations, registration by convention. Name them in the plan. **One owner per shared file in a wave**: when two tasks would edit the same file that doesn't take additions cleanly (a page listing every tab, a big switch over sections), split it in M0 into one file per section with registration by convention, or put those tasks in different waves. Hand-resolving merge conflicts on such a file cost two hours in a measured run.
- **Simplicity** (the four rules in `chadgrant:clean-code`). YAGNI: every task traces to a stated requirement; no task builds for a future one. KISS: the plan takes the simplest architecture that meets the requirements. DRY: a shared rule or type is a contract, written once in the contract task, that every other task consumes. Convention over configuration: the stack's standard layout, naming, and tooling; a deviation is an `ADR`.
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

## Phase 3: contracts first (every milestone)

No implementation is dispatched until the milestone's contracts are merged. This is where the parallel speedup comes from: once every task builds against an agreed, checked interface instead of another task's code, nothing waits on anything else, and the milestone is usually one wave. Agents building to a bare signature do about half as well as one agent doing everything; with a full written spec the gap closes.

1. **Write the contracts as code**, at their final file paths, in the language's own construct:

   | Language | Contract | Stub that compiles until implemented |
   |---|---|---|
   | TypeScript | `interface` / `type`, exported | a class that `implements` it and throws `new Error("not implemented")` |
   | Python | `typing.Protocol` or `abc.ABC` with `@abstractmethod`, fully type-hinted | a class whose methods raise `NotImplementedError` |
   | Go | `interface` | a struct whose methods `panic("not implemented")` |
   | Java · Kotlin · C# | `interface` (or abstract class) | a class that throws `UnsupportedOperationException` / `NotImplementedException` |
   | Rust | `trait` | an impl whose methods call `todo!()` |

   Data shapes (DTOs, events, error types, enums, schema types) are written in full, not stubbed.
2. **The doc comment is the spec.** Every member states its behavior, inputs, outputs, the errors it raises and when, its invariants, and one worked example, in the glossary's words. A bare signature is not a finished contract.
3. **Contract tests.** For each contract with behavior, a test suite written against the interface, run against the stub, failing for the right reason. Whoever implements the contract makes it pass; it is the reference that lets workers build without talking to each other.
4. **Wire the stubs** into the composition root (or the convention that replaces it), so the app builds and the static gate passes with every stub in place.
5. **One author.** One `general-purpose` agent, at session effort, writes all of the milestone's contracts in one task, on the mid tier (top tier when they cover `observe` work and the user approved Fable), because contracts must agree with each other. Its verify step: the static gate green, the contract tests compiling and red.
6. **You read the contract diff.** It's the one diff worth your context: check it against the milestone's `REQ`s and the glossary, and check every task in the milestone has what it consumes. Then commit it on its own (`contracts: M1`). Journal it as `phase contracts`.
7. **Contracts are frozen.** Workers never edit contract files or contract tests. A worker that needs a change finishes what it can and reports a **contract change request**. You decide: make the change yourself or as a small contract task, merge it, and mark every task that consumes or implements that contract **stale**: continue each in-flight one with `SendMessage` naming the change, and fold the change into the brief of any not yet dispatched. Record it in `STATUS.md` and `J note contract change <CON-###> <why>`. More than a couple of change requests in a milestone means the contracts were under-specified: fix that in the plan before the next milestone.
8. **Agents coordinate only through artifacts**: contracts, contract tests, the plan, and reports. Workers never message each other, and you don't relay conversation between them. Talking reduces merge conflicts but not failures; checked contracts do both.

## Phase 4: the wave loop

Repeat until the ledger is all green.

1. **Pick the wave, up to the worker cap.** At most the plan's `max_parallel` workers run at once (default 4); the rest wait for the next wave. With the contracts merged, every implementation task depends only on contracts, so the waves are limited by the cap, not by dependencies. Hold a task back only when it needs another task's running implementation, not just its contract (rare: data a migration in another task produces).
2. **Map each task before dispatch.** A small-tier `Explore` agent per task, all in one message, returns a map of at most about 40 lines: the files to create or change, with line ranges; the existing functions, components, or files to call or copy the pattern from; the tests to update and where new tests go; the wiring lines (route, registry, shell mount, help topic); the helpers to reuse. The map goes into the brief verbatim. This is the biggest lever on worker speed: in a measured run, workers whose brief named `file:line` made their first edit in 1–8 minutes, and workers whose brief only described the result spent 30–46 minutes and about 100 reads finding their way.
3. **Dispatch all in one message.** Each brief carries: the task's goal, its map, the base commit (the integration branch's current SHA, which the worker fast-forwards to first), and the `REQ`s it satisfies, the `CON`s it implements (their files and contract tests) and the ones it consumes, the fast gate command, a pointer to the plan's global constraints (the file and heading; the worker reads them there, you don't restate them), "use the `chadgrant:implementation` skill as the worker (its `worker.md`)", **never `git commit`**, **never run Docker or start backing services**, **never edit a contract file or contract test** (change requests go in the report), never edit `CLAUDE.md`, `AGENTS.md`, `STATUS.md`, or the plan (notes for those go in the report), the path to `GLOSSARY.md` when the repo has one, and the absolute report path `.delivery/<task-id>.md` with the one-line return. Dispatch with `isolation: "worktree"` and a `model:` override for the task's tier, as agent type `chadgrant:worker` for Easy and Medium tasks (it runs at medium effort, since the contracts carry the spec) and `general-purpose` (session effort) for Hard tasks.
4. **Merge the wave.** For each green task, in dependency order: `git diff --stat` its worktree (the size fits the task, nothing unrelated changed), commit its changes on its branch (you commit, not the worker), and merge the branch into the integration branch. A conflict goes to that task's worker (continue it with `SendMessage`): it merges the integration branch into its worktree, resolves, re-runs the fast gate, and reports; you commit and merge. Remove each worktree once it's merged.
5. **Verify the wave once.** Run the fast gate on the merged tree. Green verifies the wave; dispatch the next one. Red: run the failing tests' packages to find the task, and send it back to its worker. Integration and e2e tests wait for the milestone's full gate.
6. **Escalate, then re-plan.** A task that ends red: never re-dispatch the same brief at the same tier. Bump the tier when the brief was sound and the worker couldn't do it; split the task when it was too big to verify in one piece; fix the contract (Phase 3, step 7) when the interface itself was wrong. Re-plan when a task reveals new work.

## Phase 5: milestone gate

Before declaring a milestone done, run the **full gate** yourself on the merged tree: start the backing services (Docker Compose, when the project has it), run the integration tests, coverage, and e2e suite, then stop the services. Failures go back as fix tasks at the owning task's tier, each in a fresh worktree; re-run the full gate until it's green. Then `/simplify` over the accumulated diff (dedupe, dead code, collapse parallel solutions to the same concern), then review the feature.

**Review the feature, once.** One `chadgrant:code-review` in scoped mode over the milestone's accumulated diff (`git diff <milestone start>..HEAD`), on the mid tier, with the milestone's `REQ`s as the spec. When the milestone has `observe` tasks, add one top-tier reviewer for the security lens over those tasks' files. Both write to `.delivery/review-<milestone>.md` and return one line. Give each reviewer the changed-file list and a budget: the report written within about 45 minutes, findings most severe first. In a measured run, reviewers without one spent 94 minutes and 190 tool calls before writing a word.

- **Fix blockers and should-fix findings; list nits and don't fix them.** Group the findings by owning task and send each group to one worker at the task's tier, all in one message. Fixes run under [worker.md](worker.md)'s receive-review rules.
- **One round.** After the fixes, re-run the full gate. No second review: a finding still open after the fix pass is escalated under step 6 of the wave loop or recorded as deferred in `STATUS.md`.

Both gates green, note what's deferred and why, then push.

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

- **One worktree per task.** Workers never share a working tree; you commit and merge.
- **Only you run Docker.** Backing services start for the full gate and stop after it. Workers run the fast gate only, so parallel workers never compete for containers, ports, or databases.
- **Only the orchestrator commits.** Say it in every brief.
- **Only the orchestrator writes shared files**: `CLAUDE.md`, `AGENTS.md`, `STATUS.md`, the plan, the root `README`, and any doc no task owns. Workers and reviewers run in parallel and overwrite each other there, so they report notes instead. After each wave, apply the wave's **Notes for shared docs** yourself, one file at a time, merging duplicates and dropping what the file already says. A doc that a task must update (requirements docs, user docs, a package `README`) is changed by the task that changes the behavior it documents.
- **`chadgrant:worker` (Easy, Medium) or `general-purpose` (Hard, contracts), with a model override; never a fork.** A fork inherits your commit authorization.
- **Never more than `max_parallel` workers at once** (default 4), counting fix and conflict workers.
- **Verify before committing.** A worker's "tests pass" is not evidence; the green wave run is, and the bigger the diff the more it matters.
- **`STATUS.md` is the ledger**: the journal's run id, active wave, done tasks, follow-ups, incidents, decisions. Update it every wave; it's how the next context window resumes.
- **Zombie check.** A worker can die silently with no output. When nothing has changed on disk for a while, check each in-flight worktree, and the journal for an agent whose last model request is far older than the others (a stalled call or a command hung on input). A task that wrote nothing never ran, so re-dispatching the same brief is safe (the escalation rule is for tasks that ran and failed). A task that wrote partial output is treated as failed: escalate per step 6.
- **Push once per milestone**, not per task. Each push burns CI.
- **Global constraints exist before dispatch.** If the plan builds a deployable service and lacks the Twelve-Factor constraint, add it. If it lacks the test gates (90% coverage, Compose-backed services, surface-appropriate e2e), add them. Fail-mode per component class must be in the plan before dispatch: fail-closed for spend, auth, governance, budgets, safety; fail-open for soft quotas and rate limits.
