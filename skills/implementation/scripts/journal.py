#!/usr/bin/env python3
"""Delivery journal: timed events for every run, kept per project for statistics.

    journal.py begin <kind> <name> [key=value ...]   start timing something
    journal.py end   <kind> <name> [key=value ...]   stop it; the duration is recorded
    journal.py note  <text>                          a free-form note on the current run
    journal.py report [--all]                        the latest run, or every run, summarised
    journal.py path                                  where this project's journal lives

Kinds used by the skills: run, phase, wave, task, gate, review, fix.
One file per project: $CHADGRANT_JOURNAL_DIR (default ~/.claude/journal) / <repo name>.jsonl
"""
import json
import os
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_JOURNAL_DIR = Path.home() / ".claude" / "journal"
EXIT_USAGE = 2
SECONDS_PER_MINUTE = 60
GROUPED_KINDS = ("run", "wave", "task")  # named per instance, so history groups them


def project_root():
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
        return Path(out.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return Path.cwd()


def journal_path():
    directory = Path(os.environ.get("CHADGRANT_JOURNAL_DIR", DEFAULT_JOURNAL_DIR))
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{project_root().name}.jsonl"


def now():
    return datetime.now(timezone.utc)


def read_events():
    path = journal_path()
    if not path.exists():
        return []
    with path.open() as lines:
        return [json.loads(line) for line in lines if line.strip()]


def append_event(event):
    with journal_path().open("a") as journal:
        journal.write(json.dumps(event) + "\n")


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


def minutes(seconds):
    return f"{seconds / SECONDS_PER_MINUTE:7.1f}m"


def finished_events(events, run):
    return [e for e in events if e["event"] == "end" and e["run"] == run]


def describe(event):
    extras = {k: v for k, v in event.items()
              if k not in ("event", "kind", "name", "run", "at", "seconds")}
    return " ".join(f"{k}={v}" for k, v in extras.items())


def report_run(events, run):
    finished = finished_events(events, run)
    print(f"Run {run}")
    for kind in ("phase", "wave", "task", "gate", "review", "fix", "run"):
        rows = [e for e in finished if e["kind"] == kind]
        if not rows:
            continue
        total = sum(e["seconds"] for e in rows)
        print(f"  {kind} ({len(rows)}, {minutes(total).strip()} total)")
        for event in rows:
            print(f"    {minutes(event['seconds'])}  {event['name']:<28} {describe(event)}")
    for event in events:
        if event["kind"] == "note" and event["run"] == run:
            print(f"  note: {event['text']}")


def report_history(events):
    runs = sorted({e["run"] for e in events if e["run"]})
    print(f"{len(runs)} runs")
    durations = {}
    for event in events:
        if event["event"] != "end":
            continue
        what = f"{event['kind']} (each)" if event["kind"] in GROUPED_KINDS else f"{event['kind']} {event['name']}"
        durations.setdefault(what, []).append(event["seconds"])
    print(f"  {'what':<34} {'count':>5} {'median':>9} {'max':>9}")
    for what, values in sorted(durations.items()):
        print(f"  {what:<34} {len(values):>5} {minutes(statistics.median(values))} {minutes(max(values))}")


def report(all_runs):
    events = read_events()
    if not events:
        print(f"journal: nothing recorded yet in {journal_path()}")
        return
    if all_runs:
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
        report("--all" in argv[1:])
    elif argv == ["path"]:
        print(journal_path())
    else:
        print(__doc__, file=sys.stderr)
        sys.exit(EXIT_USAGE)


if __name__ == "__main__":
    main(sys.argv[1:])
