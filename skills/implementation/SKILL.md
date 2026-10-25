---
name: implementation
description: Execute an existing implementation plan or task brief, either coordinating a multi-task build or implementing and verifying one assigned task. Includes debugging and review fixes within that delivery; excludes authoring requirements or plans from scratch.
---

# Implementation

Choose your role and read only its manual. Code standards come from [clean-code](../clean-code/SKILL.md); requirements and plans come from `chadgrant:planning`.

| Role | Read |
|---|---|
| Delivering a multi-task plan | [orchestrator.md](orchestrator.md) |
| Assigned a task, including a Fork of the orchestrator | [worker.md](worker.md) |
| Implementing one self-evident task alone | [worker.md](worker.md), using the solo exception below |

Prefer **Forks whenever available** for delegation; use [delegation.md](delegation.md) for context reuse, worktree isolation, and model/tool fallbacks. A forked worker remains a worker despite inheriting the orchestrator's conversation.

## Shared rules

- **Delegated workers:** one worktree per task; only the orchestrator creates commits, merges into the integration branch, runs Docker/backing services, or edits shared files (`CLAUDE.md`, `AGENTS.md`, `STATUS.md`, the plan, root `README`, unowned docs). Workers may fast-forward their own worktree to the supplied base or merge the integration branch into it for conflict recovery without creating a commit. Workers report proposed shared-doc changes.
- **Contracts first:** merge milestone interfaces, shared types, doc-comment specs, stubs, and contract tests before parallel implementation. Workers never edit frozen contracts/tests or bypass them; report contract change requests. Coordinate through these artifacts and reports, not worker-to-worker messages.
- **Verification:** workers run the fast gate; the orchestrator runs the full gate with real backing services where applicable, at least 90% coverage, and surface-appropriate e2e. Reports contain actual evidence.
- **Context:** full reports go to `.delivery/<id>.md`; return one-line status and path. Read only relevant skill sections and task files; avoid reloading inherited, unchanged context.
- **Environment limits:** distinguish code-complete/tested-with-fakes from production-verified; provide a runbook for unavailable live steps.
- **Solo exception:** with no delegation, use the existing checkout unless isolation is needed; you own necessary files and verification. Commit only when requested. Do not require a worktree, formal contracts, ledger, or orchestrator handoff for a self-evident task.
