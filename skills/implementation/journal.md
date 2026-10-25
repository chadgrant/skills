# Delivery journal

`J` means `python3 <implementation skill directory>/scripts/journal.py`. Events append to `~/.claude/journal/<repo name>.jsonl`; `J path` prints the path. Reuse stable event names to compare runs.

Hooks record briefs, skill loads, main-session turns, subagent timing/tokens/model/provider, API failures, and skill version/commit. Do not duplicate those events. Add only the semantic events below. `J report --timeline` shows gaps, `--providers` compares providers, `--versions` compares skill revisions, and `--all` compares runs.

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
