---
name: implementation
description: Use when building from a plan or a brief. As the orchestrator: delivering a multi-task build (a project, milestone, or migration) by running waves of subagents whose results are verified and committed. As the worker: building one task from a plan or a dispatched brief. Triggers: "build the plan", "contracts first", "run the waves", "orchestrate this", "execute IMPLEMENTATION.md", "implement TASK-###", "build this task", "you are the worker", "the test is failing", "address the review". Not for writing the requirements or the plan.
---

# Implementation

One skill, two roles. Find yours, open that file, and follow it. Don't read the other one; it isn't your job and it costs context.

| You are | Open |
|---|---|
| Delivering a plan with more than one task, dispatching subagents | [orchestrator.md](orchestrator.md) |
| A subagent handed a brief, or told "you are the worker" | [worker.md](worker.md) |
| Building one self-evident task alone, with no plan and no subagents | [worker.md](worker.md). You hold both roles: every file is yours, and you commit when the user asks. |

Pipeline: `chadgrant:planning` writes the docs and the routed plan → **`chadgrant:implementation`** builds it → `chadgrant:code-review` reviews it. The standards for the code itself are `chadgrant:clean-code`'s.

## Rules for both roles

- **One worktree per task.** Workers change what their feature needs in their own worktree; the orchestrator merges. `CLAUDE.md`, `AGENTS.md`, `STATUS.md`, the plan, and the root `README` belong to the orchestrator alone; workers and reviewers report notes for them.
- **Only the orchestrator runs Docker.** Workers run the fast gate (unit tests, static checks); the full gate with backing services runs once per milestone.
- **Contracts first.** Every milestone starts with its interfaces, abstract classes, and shared types written as code, with doc-comment specs, stubs, and contract tests, merged before any implementation is dispatched. Workers build against contracts and never change them; agents coordinate only through these artifacts, never by messaging each other.
- **Only the orchestrator commits.**
- **Reports on disk, one line back.** Full reports go to `.delivery/<id>.md`; what returns to the caller is one line.
- **Evidence, not claims.** A task is done when its fast gate is actually green. A milestone is done when the full gate is green: integration tests against real backing services where the project has them, coverage at or above 90%, e2e.
- **Honest environment ceiling.** Without real cloud, certs, or live services, "done" means code-complete, tested with fakes, plus a runbook for the real step. Never imply production-verified.

---

*Structure, debug loop, and review discipline inspired by [obra/superpowers](https://github.com/obra/superpowers).*
