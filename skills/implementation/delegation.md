# Delegation: prefer Forks

Use **Forks whenever available** for implementation, investigation, and review that can reuse the current context. Check the available Agent tool capabilities; do not assume a client supports them or change user settings to enable them.

Claude Code Forks inherit the parent's conversation, system prompt, tools, and model. Their first request can reuse the parent's prompt cache; subsequent tool output stays in the fork and its result returns to the parent. This is inherited context at launch, not live synchronization between workers. `isolation: "worktree"` gives a fork a separate checkout. See [Claude's Fork documentation](https://code.claude.com/docs/en/sub-agents#fork-the-current-conversation).

## Dispatch

- When supported, use `subagent_type: "fork"`; add `isolation: "worktree"` for edits. Forks inherit the session model: do not attach a different model or custom-worker effort override.
- State the new role explicitly: “You are the worker for TASK-###; follow implementation/worker.md.” Include the task, base SHA, scope, contract IDs, fast gate, and absolute report path. Refer to inherited requirements and decisions instead of pasting them again.
- Retain a short boundary line even in a Fork brief: **no commits, Docker/backing services, shared-doc edits, or frozen-contract/test edits; report change requests**. Inherited tools are capabilities, not permission to act as the orchestrator.
- Keep contracts and reports authoritative. Notify affected workers of contract updates; a fork does not automatically see later conversation changes. Count forks toward `max_parallel` and return the same compact reports.

## Fallbacks and cost

Use a non-fork subagent when Forks are unavailable, a required model/effort differs from the parent, or restricted tools/fresh context are necessary. Follow [routing.md](routing.md); use `chadgrant:worker` for Easy/Medium implementation and `general-purpose` for Hard work or contracts. An independent review may need fresh context to avoid inheriting the implementer's conclusions.

Do not spawn an agent for a lookup that one bounded local command resolves. Prefer resuming the existing worker for follow-ups. Cache reuse can reduce repeated input cost, but a fork still inherits the context and consumes tokens; compare journal results instead of assuming a fixed saving.

Skill frontmatter `context: fork` is a separate mechanism: it runs the skill in a subagent without inheriting conversation history. Do not add it as a substitute for a conversation Fork. See [running skills in a subagent](https://code.claude.com/docs/en/skills#run-skills-in-a-subagent).
