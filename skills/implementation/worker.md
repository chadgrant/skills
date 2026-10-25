# Worker: build one task

Announce the worker role. Implement the brief, run its fast gate, and report evidence. Delegated workers follow the shared rules in [SKILL.md](SKILL.md), even when forked from the orchestrator. For solo work, use the solo exception there; do not invent a dispatch brief or contracts.

## Establish the task

Read the goal, map (files/ranges, reusable code, tests, wiring), base SHA, implemented/consumed `CON`s, verify command, global-constraints pointer, and report path. Read only the relevant architecture note, glossary, contracts, tests, and source ranges. Reuse context already inherited by a Fork; re-read files only when changed or needed to verify current state.

A delegated worker starts in its own worktree: `git merge --ff-only <base SHA>`, then follow the repo's setup instructions. Report a failed fast-forward instead of building on a stale base. Bound installs/network calls with a timeout and avoid interactive commands.

For a gap that does not affect interfaces or observable behavior, choose the smallest defensible interpretation and record `⚠`. If it changes behavior, ask the orchestrator; continue independent work. A wrong or incomplete frozen contract requires a **contract change request**, never an edit or a workaround using casts, `any`, extra public methods, or another module's internals.

## Build and verify

1. **Verify-first:** make the existing contract tests pass. For uncovered behavior, add a failing test and implementation one slice at a time. Assert through the public interface with independent expected values. Scaffolding/config tasks whose verify step is build/lint/type-check need no invented test.
2. **Reuse:** search the repo, framework, standard library, and existing dependencies before writing a helper or adding a package. Apply [clean-code](../clean-code/SKILL.md); read a design catalog only when a concrete decision needs it.
3. **Dependencies:** resolve the latest stable release through the registry or the package manager's unversioned add command (`npm install <pkg>`, `pnpm add`, `uv add`, `poetry add`, `cargo add`, `dotnet add package`; Go uses `go get <module>@latest`). Never type a version from memory. Exclude prereleases; if compatibility requires an older version, record the reason under `⚠`. Update manifest and lockfile together for the orchestrator to commit.
4. **Surface constraints:** for UI, use the brief's Impeccable skill and the style guide's `TOK-`/`CMP-` with the wireframes. For a deployable service, read [services.md](services.md). Report unavailable tools or unmet constraints rather than silently claiming compliance.
5. **Tests:** cover at least 90% of added/changed lines through behavioral assertions; exclusions must be in the plan. Write integration tests against real backing services and e2e scenarios using the plan's driver (browser → Playwright; API → HTTP; CLI → built binary). The orchestrator runs these in the full gate; delegated workers run only self-contained tests and static checks.
6. **Prove and tidy:** run the exact fast gate, inspect your diff for scope, clarity, duplication, and unnecessary machinery, fix issues, then re-run affected verification. Report actual commands/results. This is a self-check; the feature review happens at the milestone gate.

Keep reads targeted (`rg -n`, file ranges, bounded output). If discovery spans roughly 15 files without locating an edit, identify the missing map information, continue where possible, and report the gap.

## Debugging and review fixes

Reproduce the failure, read the actual error, then test one reasoned hypothesis at a time. Fix the root cause and re-verify without weakening tests. After three or four failed hypotheses, or when a fix needs out-of-scope changes, report attempts and escalate. If a failure cannot be reproduced, report that uncertainty rather than masking it. Use [investigation](../investigation/SKILL.md) for a substantial causal trace; it does not relax worker boundaries.

For each review finding, reproduce or trace it before editing. Report **fixed** with verification evidence, **refuted** with counter-evidence, or **unresolved** with the missing check/blocker. Do not implement a finding merely because a reviewer asserted it.

## Report

Write about 25 lines per task to the brief's absolute report path, with no pasted code or full logs:

- **Task / files changed:** ID, base/tested revision (including uncommitted changes), changed paths, and explanations for unexpected paths.
- **Contracts implemented:** `CON` IDs and contract-test pass counts.
- **Contract change requests:** contract, proposed change, reason; omit if none.
- **Verify:** command, exit status, pass/fail counts, measured coverage if available. Include failure details only for unresolved failures; do not claim full-gate results you did not run.
- **Quality:** self-check outcome and refactoring, one or two lines.
- **Deviations / ⚠:** assumptions, map gaps, unmet constraints, and unverifiable steps with a runbook.
- **Notes for shared docs:** target file and exact proposed text for the orchestrator; omit if none.
- **Review response:** fixed/refuted evidence or unresolved check per finding, only after a review.

Return only: `TASK-### · green|red · <verify summary> · ⚠ <count> · notes <count> · contract changes <count> · <report path>`. With no report path, return the report itself.
