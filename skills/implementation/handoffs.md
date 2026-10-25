# Evidence across skills

Read only when passing work between skills or sessions. Extend the existing brief/report; do not create a second ledger or duplicate the requirements. A small standalone task can return these fields in prose.

- **Scope:** goal, changed files, existing `REQ`/`NFR`/`CON`/`TASK`/`TEST`/`TC` IDs where present; do not invent IDs for a simple fix.
- **State:** base and tested revision, dirty-tree changes if any, build/environment, authoritative plan and report paths.
- **Evidence:** exact commands, exit status and observed results, artifact paths, and unavailable checks. Rerun affected checks when their code or environment changes.
- **Decisions:** accepted constraints, unresolved risks/findings, contract change requests, next action and owner.
- **Authorization:** already-approved actions and limits. Preserve existing authorization; a handoff neither resets it nor expands it. Push/local install does not imply deployment, monitoring, or contacting others.

Investigation supplies evidence to planning or an understood fix. Planning supplies contracts and acceptance criteria to implementation. Verification adds runtime evidence to the full gate. Review returns scoped findings to implementation for fixes and affected rechecks. Clean-code standards apply throughout; do not invoke every skill for every task.

Delegated workers remain unable to own shared services, shared docs, commits, or integration merges regardless of which skill they use. Read the detailed evidence only when the compact return flags a failure, uncertainty, or decision.
