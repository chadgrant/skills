#!/usr/bin/env python3
"""Delivery journal: timed events for every run, kept per project for statistics.

    journal.py begin <kind> <name> [key=value ...]   start timing something
    journal.py end   <kind> <name> [key=value ...]   stop it; the duration is recorded
    journal.py note  <text>                          a free-form note on the current run
    journal.py report [--all | --providers | --versions]  latest run, every run, providers, or skill versions compared
    journal.py path                                  where this project's journal lives
    journal.py hook                                  called by the plugin's hooks with the event on stdin

Kinds used by the skills: run, phase, wave, task, gate, review, fix.
Kinds written by the hooks: agent (one per subagent), api_error.
Every event carries the skills' version and git commit, so changes to the skills can be compared.
One file per project: $CHADGRANT_JOURNAL_DIR (default ~/.claude/journal) / <repo name>.jsonl
"""
import json
import os
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import transcript  # noqa: E402  (sits beside this script)
import version  # noqa: E402

DEFAULT_JOURNAL_DIR = Path.home() / ".claude" / "journal"
EXIT_USAGE = 2
SECONDS_PER_MINUTE = 60
GROUPED_KINDS = ("run", "wave", "task", "agent")  # named per instance, so history groups them
P90 = 0.9


def project_root(cwd=None):
    """The main checkout's root, so a worktree logs to the same journal as its repository."""
    directory = Path(cwd) if cwd else Path.cwd()
    try:
        out = subprocess.run(
            ["git", "-C", str(directory), "rev-parse", "--path-format=absolute", "--git-common-dir"],
            capture_output=True, text=True, check=True)
        return Path(out.stdout.strip()).parent
    except (subprocess.CalledProcessError, FileNotFoundError):
        return directory


def journal_path(cwd=None):
    directory = Path(os.environ.get("CHADGRANT_JOURNAL_DIR", DEFAULT_JOURNAL_DIR))
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{project_root(cwd).name}.jsonl"


def now():
    return datetime.now(timezone.utc)


def read_events(cwd=None):
    path = journal_path(cwd)
    if not path.exists():
        return []
    with path.open() as lines:
        return [json.loads(line) for line in lines if line.strip()]


def append_event(event, cwd=None):
    with journal_path(cwd).open("a") as journal:
        journal.write(json.dumps({**event, **version.skills()}) + "\n")


def parse_fields(pairs):
    fields = {}
    for pair in pairs:
        key, separator, value = pair.partition("=")
        if not separator:
            raise SystemExit(f"journal: expected key=value, got '{pair}'")
        fields[key] = value
    return fields


def current_run(events):
    runs = [e for e in events if e["kind"] == "run" and e["event"] == "begin"]
    return runs[-1]["name"] if runs else None


def open_begin(events, kind, name):
    ended = 0
    for event in reversed(events):
        if event["kind"] != kind or event["name"] != name:
            continue
        if event["event"] == "end":
            ended += 1
        elif ended:
            ended -= 1
        else:
            return event
    return None


def begin(kind, name, fields):
    events = read_events()
    run = name if kind == "run" else current_run(events)
    if kind == "run":
        fields.setdefault("path", str(project_root()))
        fields.setdefault("provider", transcript.provider())
    append_event({"event": "begin", "kind": kind, "name": name, "run": run,
                  "at": now().isoformat(), **fields})


def end(kind, name, fields):
    events = read_events()
    started = open_begin(events, kind, name)
    if started is None:
        raise SystemExit(f"journal: no open '{kind} {name}' to end")
    finished = now()
    seconds = (finished - datetime.fromisoformat(started["at"])).total_seconds()
    append_event({"event": "end", "kind": kind, "name": name, "run": started["run"],
                  "at": finished.isoformat(), "seconds": round(seconds), **fields})


def note(text):
    events = read_events()
    append_event({"event": "note", "kind": "note", "name": "", "run": current_run(events),
                  "at": now().isoformat(), "text": text})


# --- hooks: one event per subagent, and one per API failure, with no help from the agent ---

def hook_event(payload, kind, event, **fields):
    cwd = payload.get("cwd")
    append_event({"event": event, "kind": kind, "name": payload.get("agent_id", ""),
                  "run": current_run(read_events(cwd)), "at": now().isoformat(),
                  "agent_type": payload.get("agent_type", ""), "session": payload.get("session_id", ""),
                  "provider": transcript.provider(), **fields}, cwd)


def on_subagent_stop(payload):
    path = payload.get("agent_transcript_path")
    stats = transcript.summarize(path) if path else {}
    hook_event(payload, "agent", "end", **stats)


def on_stop_failure(payload):
    hook_event(payload, "api_error", "note", error=payload.get("error", "unknown"),
               details=str(payload.get("error_details", ""))[:300])


HOOK_HANDLERS = {
    "SubagentStart": lambda payload: hook_event(payload, "agent", "begin"),
    "SubagentStop": on_subagent_stop,
    "StopFailure": on_stop_failure,
}


def hook():
    """Never fails the session: a journal problem is not worth interrupting work for."""
    try:
        payload = json.load(sys.stdin)
        handler = HOOK_HANDLERS.get(payload.get("hook_event_name"))
        if handler:
            handler(payload)
    except Exception as error:  # noqa: BLE001
        print(f"journal hook: {error}", file=sys.stderr)


# --- reports ---

def minutes(seconds):
    return f"{seconds / SECONDS_PER_MINUTE:7.1f}m"


def percentile(values, fraction):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(fraction * len(ordered)))]


def describe(event):
    extras = {k: v for k, v in event.items()
              if k not in ("event", "kind", "name", "run", "at", "seconds", "session",
                           "skills_version", "skills_commit")}
    return " ".join(f"{k}={v}" for k, v in extras.items())


def report_run(events, run):
    finished = [e for e in events if e["event"] == "end" and e["run"] == run]
    print(f"Run {run}")
    for kind in ("phase", "wave", "task", "agent", "gate", "review", "fix", "run"):
        rows = [e for e in finished if e["kind"] == kind]
        if not rows:
            continue
        total = sum(e.get("seconds", 0) for e in rows)
        print(f"  {kind} ({len(rows)}, {minutes(total).strip()} total)")
        for event in rows:
            print(f"    {minutes(event.get('seconds', 0))}  {event['name']:<28} {describe(event)}")
    for event in events:
        if event["run"] == run and event["kind"] in ("note", "api_error"):
            print(f"  {event['kind']}: {event.get('text') or event.get('error')} {event.get('details', '')}")


def report_history(events):
    runs = sorted({e["run"] for e in events if e["run"]})
    print(f"{len(runs)} runs")
    durations = {}
    for event in events:
        if event["event"] != "end":
            continue
        what = f"{event['kind']} (each)" if event["kind"] in GROUPED_KINDS else f"{event['kind']} {event['name']}"
        durations.setdefault(what, []).append(event.get("seconds", 0))
    print(f"  {'what':<34} {'count':>5} {'median':>9} {'max':>9}")
    for what, values in sorted(durations.items()):
        print(f"  {what:<34} {len(values):>5} {minutes(statistics.median(values))} {minutes(max(values))}")


def report_providers(events):
    """Subagent speed and failures per provider: is the slowness in the model, or in the work?"""
    print(f"  {'provider':<10} {'agents':>6} {'unfinished':>10} {'api errors':>10} "
          f"{'median':>9} {'p90':>9} {'model share':>11} {'s/request':>9} {'out tok/s':>9}")
    for name in sorted({e.get("provider") for e in events if e["kind"] in ("agent", "api_error")} - {None}):
        mine = [e for e in events if e.get("provider") == name]
        ended = [e for e in mine if e["kind"] == "agent" and e["event"] == "end" and e.get("seconds")]
        started = sum(1 for e in mine if e["kind"] == "agent" and e["event"] == "begin")
        errors = sum(1 for e in mine if e["kind"] == "api_error") + sum(e.get("api_errors", 0) for e in ended)
        if not ended:
            print(f"  {name:<10} {started:>6} {started:>10} {errors:>10}")
            continue
        seconds = [e["seconds"] for e in ended]
        model_seconds = sum(e.get("model_seconds", 0) for e in ended)
        requests = sum(e.get("requests", 0) for e in ended) or 1
        output = sum(e.get("tokens_output", 0) for e in ended)
        print(f"  {name:<10} {len(ended):>6} {max(0, started - len(ended)):>10} {errors:>10} "
              f"{minutes(statistics.median(seconds))} {minutes(percentile(seconds, P90))} "
              f"{model_seconds / max(1, sum(seconds)):>10.0%} {model_seconds / requests:>9.1f} "
              f"{output / max(1, model_seconds):>9.1f}")


def outcome_count(events, kind, outcomes):
    return sum(1 for e in events if e["kind"] == kind and e["event"] == "end" and e.get("outcome") in outcomes)


def median_seconds(events, kind):
    values = [e.get("seconds", 0) for e in events if e["kind"] == kind and e["event"] == "end"]
    return minutes(statistics.median(values)).strip() if values else "-"


def field_total(events, kind, field):
    return sum(int(e.get(field, 0)) for e in events if e["kind"] == kind and e["event"] == "end")


def report_versions(events):
    """How each version of the skills performed: speed, rework, review findings, failures."""
    print(f"  {'skills':<22} {'runs':>4} {'tasks':>5} {'task med':>8} {'red/esc':>7} {'agent med':>9} "
          f"{'full red':>8} {'blockers':>8} {'should-fix':>10} {'api err':>7}")
    for commit in sorted({e.get("skills_commit", "unknown") for e in events}):
        mine = [e for e in events if e.get("skills_commit", "unknown") == commit]
        label = f"{mine[0].get('skills_version', '?')}@{commit}"
        tasks = sum(1 for e in mine if e["kind"] == "task" and e["event"] == "end")
        full_gates = [e for e in mine if e["kind"] == "gate" and e["name"] == "full" and e["event"] == "end"]
        print(f"  {label:<22} {sum(1 for e in mine if e['kind'] == 'run' and e['event'] == 'begin'):>4} "
              f"{tasks:>5} {median_seconds(mine, 'task'):>8} "
              f"{outcome_count(mine, 'task', ('red', 'escalated')):>7} {median_seconds(mine, 'agent'):>9} "
              f"{sum(1 for e in full_gates if e.get('outcome') == 'red')}/{len(full_gates):<6} "
              f"{field_total(mine, 'review', 'blockers'):>8} {field_total(mine, 'review', 'should_fix'):>10} "
              f"{sum(1 for e in mine if e['kind'] == 'api_error') + field_total(mine, 'agent', 'api_errors'):>7}")


def report(flags):
    events = read_events()
    if not events:
        print(f"journal: nothing recorded yet in {journal_path()}")
    elif "--versions" in flags:
        report_versions(events)
    elif "--providers" in flags:
        report_providers(events)
    elif "--all" in flags:
        report_history(events)
    else:
        report_run(events, current_run(events))


def main(argv):
    if len(argv) >= 3 and argv[0] in ("begin", "end"):
        action = begin if argv[0] == "begin" else end
        action(argv[1], argv[2], parse_fields(argv[3:]))
    elif len(argv) >= 2 and argv[0] == "note":
        note(" ".join(argv[1:]))
    elif argv and argv[0] == "report":
        report(argv[1:])
    elif argv == ["path"]:
        print(journal_path())
    elif argv == ["hook"]:
        hook()
    else:
        print(__doc__, file=sys.stderr)
        sys.exit(EXIT_USAGE)


if __name__ == "__main__":
    main(sys.argv[1:])
