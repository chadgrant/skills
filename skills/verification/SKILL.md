---
name: verification
description: Prove behavior through an application's real user or public API surface, or create a reusable project verification recipe. Use for runtime evidence and launch/drive/cleanup workflows; routine unit-test execution needs no separate skill.
---

# Verification

Prove the requested behavior on an identified build. Reuse the project's harness and verification instructions. If repeatable instructions are missing or requested, read [project-recipe.md](project-recipe.md) and create only the recipe needed for this scope.

## Run a proof

1. **Scope:** identify the behavior, acceptance criterion, revision (including uncommitted changes), environment, and available driver. Browser UI → browser automation; API → public HTTP endpoint; CLI → built command/PTY; library → public API. Keep existing `REQ`/`TEST`/`TC` IDs.
2. **Prepare:** inspect launch/setup commands before executing them. Use isolated test data and record resources created by this run. Delegated workers retain their file/service restrictions: propose shared recipe edits to the orchestrator, never start backing services or run the full gate. The orchestrator or solo agent owns service lifecycle.
3. **Launch and diagnose:** reach usable readiness, including migrations, seed data, and authentication. A listening port alone is insufficient. Confirm the expected build and instance with a read-only diagnostic check before driving it; failures need diagnosis, not blind restarts.
4. **Drive:** perform the real action and assert its observable result and relevant side effects. A final screenshot alone is not proof of the action. Do not substitute internal setters, test-only endpoints, or mocks for the behavior being claimed. Identify external boundaries replaced by fakes and limit the claim accordingly. Inspect dry-run/test-mode behavior before assuming it has no external effects.
5. **Capture:** store commands, exit codes, expected/actual results, and relevant screenshots, responses, or state checks under the supplied evidence path, otherwise `.delivery/verification/<run-id>/`. Keep evidence outside disposable state, redact secrets, and capture failure diagnostics too.
6. **Clean up:** on success or failure, remove only resources this run created, using recorded process/container/session identities. Never kill by process name or remove shared volumes. Confirm evidence still exists after cleanup and report any resources left running.

## Report

State **passed**, **failed**, or **blocked**, then the verified behavior/build, environment, commands/results, evidence paths, cleanup outcome, and unverified gaps. Passing unit tests or a substitute environment does not prove an unavailable live path. For blocked steps, provide the exact remaining runbook without claiming success.

Use [handoffs.md](../implementation/handoffs.md) for a delivery report. Failures return to [implementation](../implementation/SKILL.md), or [investigation](../investigation/SKILL.md) when the cause is unclear. Evidence accompanies the existing [code-review](../code-review/SKILL.md) handoff; do not add an overlapping review or infer deployment authorization from a passing proof.
