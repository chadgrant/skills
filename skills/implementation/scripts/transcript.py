"""Reads a subagent transcript into timing, token, and error statistics, and names the API provider."""
import json
import os
import re
from datetime import datetime

TASK_ID = re.compile(r"\bTASK-\d+\b")
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
READ_TOOLS = {"Read", "Grep", "Glob"}
SHELL_READ = re.compile(r"(^|&&|;|\|)\s*(grep|rg|sed -n|cat|head|tail|find|ls|wc)\b")
SYNTHETIC_MODEL = "<synthetic>"  # Claude Code's model name on messages it writes for API errors


def provider():
    """The API provider this Claude Code process talks to, from its environment."""
    if os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1":
        return "bedrock"
    if os.environ.get("CLAUDE_CODE_USE_VERTEX") == "1":
        return "vertex"
    if os.environ.get("CLAUDE_CODE_USE_FOUNDRY") == "1":
        return "foundry"
    if os.environ.get("ANTHROPIC_BASE_URL"):
        return "gateway"
    return "anthropic"


def timestamp(entry):
    return datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))


def read_entries(path):
    entries = []
    with open(os.path.expanduser(path)) as lines:
        for line in lines:
            if line.strip():
                entry = json.loads(line)
                if "timestamp" in entry:
                    entries.append(entry)
    return entries


def first_prompt(entries):
    for entry in entries:
        if entry.get("type") == "user":
            content = entry.get("message", {}).get("content")
            return content if isinstance(content, str) else json.dumps(content)
    return ""


def is_api_error(entry):
    message = entry.get("message", {})
    return bool(entry.get("isApiErrorMessage")) or message.get("model") == SYNTHETIC_MODEL


class Requests:
    """One model request per distinct message id; its wait is the gap since the entry before it."""

    def __init__(self):
        self.seen = set()
        self.count = 0
        self.wait_seconds = 0.0
        self.tokens = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0}
        self.models = set()
        self.errors = 0
        self.peak_context = 0

    def add(self, entry, previous):
        if is_api_error(entry):
            self.errors += 1
            return
        message = entry.get("message", {})
        if message.get("id") in self.seen:
            return
        self.seen.add(message.get("id"))
        self.count += 1
        self.models.add(message.get("model", "unknown"))
        if previous is not None:
            self.wait_seconds += (timestamp(entry) - timestamp(previous)).total_seconds()
        self.add_usage(message.get("usage", {}))

    def add_usage(self, usage):
        self.tokens["input"] += usage.get("input_tokens", 0)
        self.tokens["output"] += usage.get("output_tokens", 0)
        self.tokens["cache_read"] += usage.get("cache_read_input_tokens", 0)
        self.tokens["cache_write"] += usage.get("cache_creation_input_tokens", 0)
        context = (usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0)
                   + usage.get("cache_creation_input_tokens", 0))
        self.peak_context = max(self.peak_context, context)


def tool_uses(entry):
    content = entry.get("message", {}).get("content")
    return [block for block in content if block.get("type") == "tool_use"] if isinstance(content, list) else []


def is_read(tool):
    if tool.get("name") in READ_TOOLS:
        return True
    return tool.get("name") == "Bash" and bool(SHELL_READ.search(tool.get("input", {}).get("command", "")))


def first_edit(entries):
    """Seconds from the start to the first file edit, and how many reads came before it."""
    reads = 0
    for entry in entries:
        for tool in tool_uses(entry):
            if tool.get("name") in EDIT_TOOLS:
                return round((timestamp(entry) - timestamp(entries[0])).total_seconds()), reads
            reads += is_read(tool)
    return None, reads


def summarize(path):
    """Wall time, model wait, requests, tokens, peak context, time to first edit, models, API errors, task id."""
    entries = read_entries(path)
    if not entries:
        return {}
    requests = Requests()
    previous = None
    for entry in entries:
        if entry.get("type") == "assistant":
            requests.add(entry, previous)
        previous = entry
    task = TASK_ID.search(first_prompt(entries))
    first_edit_seconds, reads_before_first_edit = first_edit(entries)
    return {
        "seconds": round((timestamp(entries[-1]) - timestamp(entries[0])).total_seconds()),
        "model_seconds": round(requests.wait_seconds),
        "requests": requests.count,
        "api_errors": requests.errors,
        "peak_context": requests.peak_context,
        "first_edit_seconds": first_edit_seconds,
        "reads_before_first_edit": reads_before_first_edit,
        "model": ",".join(sorted(requests.models)),
        "task": task.group(0) if task else "",
        **{f"tokens_{name}": count for name, count in requests.tokens.items()},
    }
