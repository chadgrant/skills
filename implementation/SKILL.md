---
name: implementation
description: Use when building from a plan or a brief. As the orchestrator: delivering a multi-task build (a project, milestone, or migration) by running waves of subagents whose results are verified and committed. As the worker: building one task from a plan or a dispatched brief. Triggers: "build the plan", "run the waves", "orchestrate this", "execute IMPLEMENTATION.md", "implement TASK-###", "build this task", "you are the worker", "the test is failing", "address the review". Not for writing the requirements or the plan.
---

# Implementation

One skill, two roles. Find yours, open that file, and follow it. Don't read the other one; it isn't your job and it costs context.

| You are | Open |
|---|---|
| Delivering a plan with more than one task, dispatching subagents | [orchestrator.md](orchestrator.md) |
| A subagent handed a brief, or told "you are the worker" | [worker.md](worker.md) |
| Building one self-evident task alone, with no plan and no subagents | [worker.md](worker.md). You hold both roles: every file is yours, and you commit when the user asks. |

Pipeline: `planning` writes the docs and the routed plan → **`implementation`** builds it → `clean-code-review` reviews it. The standards for the code itself are `uncle-bob-clean-code`'s.

## Rules for both roles

- **One writer per file.** Each task owns its files. `CLAUDE.md`, `AGENTS.md`, `STATUS.md`, the plan, and the root `README` belong to the orchestrator; workers and reviewers report notes for them.
- **Only the orchestrator commits.**
- **Reports on disk, one line back.** Full reports go to `.delivery/<id>.md`; what returns to the caller is one line.
- **Evidence, not claims.** "Done" is the verify command's actual result, green, with coverage at or above 90%, against real backing services.
- **Honest environment ceiling.** Without real cloud, certs, or live services, "done" means code-complete, tested with fakes, plus a runbook for the real step. Never imply production-verified.

---

*Structure, debug loop, and review discipline inspired by [obra/superpowers](https://github.com/obra/superpowers).*
