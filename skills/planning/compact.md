# Path D: compact requirements

**The docs state what is true now. Git holds how they got there.** Every agent that reads a doc pays for all of it, so history inside a doc is a cost on every later task.

**When a requirement changes**, edit it where it stands and keep its ID. The only trace left in the doc is one dated line in a `## Recent changes` section at the end of that doc: `2026-10-11 · REQ-012 · rate limit raised from 60 to 100/min · TASK-031`. That section exists so in-flight tasks and reviewers can see what moved; it is not a record.

**The cutoff.** A `Recent changes` entry is deleted when the milestone that implemented it has shipped, or when it is 14 days old, whichever comes first. A doc never carries more than ten entries; past that, the oldest go. `chadgrant:implementation` runs this at each milestone gate; run it yourself any time a doc reads like a log.

**Compacting a doc that has already bloated** (amendments appended at the end, "UPDATE:" notes, struck-through text, version tables, chains of superseded decisions):

1. **Fold each change into the item it changes.** The item's text becomes the current truth, under its original ID. The amendment, note, or strike-through is deleted.
2. **Collapse superseded decisions.** The surviving `ADR` keeps its number and gains one line, `Replaces: <what was decided before, and why it changed>`. The superseded `ADR` is deleted. References to the old number are repointed to the survivor.
3. **Remove what was dropped.** A requirement, entity, or endpoint that no longer exists is deleted, and its ID goes on a single `Retired IDs:` line at the end of the doc so it is never reused.
4. **Merge duplicates.** Two items that now say the same thing become one; the dropped ID is retired and its references repointed.
5. **Clear `Recent changes`** down to the entries still inside the cutoff.
6. **Run the [traceability checklist](document-rules.md#traceability-checklist) for affected IDs.** Every ID still referenced anywhere (docs, plan, code comments, tests) resolves, or is on a `Retired IDs` line.

Compaction changes no meaning. If folding a change in would alter what was promised, or two changes contradict each other, that is a question for the user, not a compaction. When committing is authorized, keep compaction in its own commit.
