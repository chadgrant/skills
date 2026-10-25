# Host adapters

Read only when translating delegation or tool calls between hosts. The active tool schema, session instructions, and user choices take precedence over examples. Missing tools do not justify changing permissions or configuration.

| Operation | Claude Code | Codex / hosted Codex |
|---|---|---|
| Invoke a skill | `chadgrant:<name>` through the Skill tool when exposed | `$<name>` or read its discovered `SKILL.md`; do not assume a Claude Skill tool |
| Delegate with history | Agent `subagent_type: "fork"` when exposed | Inspect `spawn_agent` for a history control; on hosts exposing `fork_turns`, use `"all"`. Never assume a field exists |
| Independent review | Fresh non-fork reviewer with requirements, diff and raw evidence | Select fresh context through the exposed control (`fork_turns: "none"` on hosts supporting it), supplying the same minimal review inputs |
| Isolate edits | Agent `isolation: "worktree"` when supported | Create a separate Git worktree and give its absolute path; verify the worker uses it unless the host explicitly provides isolation |
| Follow-up | Resume/message the existing agent using exposed tools | Use the exposed resume/send/follow-up tool with the agent ID; follow that tool's wake-up semantics |
| Ask a material question | Structured question tool when exposed | Structured question tool when exposed and allowed in the active mode; otherwise ask in text |

Without delegation tools or authorization, work sequentially. Do not send Claude model aliases or agent types to Codex. Use the host's available model identifiers only when a model override is needed and authorized; inherited-context agents retain the parent configuration where required by the tool. Session `codex fork` and skill frontmatter `context: fork` are not substitutes for a live subagent tool.

References: [Claude subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Codex skills](https://learn.chatgpt.com/docs/build-skills). Verify capabilities in the running client rather than treating a documented feature as universally available.
