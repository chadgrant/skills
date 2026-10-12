"""Which version of the skills is running: the plugin version and the git commit it was built from."""
import functools
import json
import subprocess
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
INSTALLED_PLUGINS = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
SHORT_SHA = 12


def git(*args):
    return subprocess.run(["git", "-C", str(PLUGIN_ROOT), *args],
                          capture_output=True, text=True, check=True).stdout.strip()


def commit_from_checkout():
    """A working copy of the skills repo: its HEAD, marked dirty when it has uncommitted changes."""
    try:
        sha = git("rev-parse", "HEAD")[:SHORT_SHA]
        return f"{sha}-dirty" if git("status", "--porcelain", "--", ".") else sha
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def commit_from_install():
    """An installed plugin: the commit Claude Code recorded when it installed this copy."""
    try:
        installs = json.loads(INSTALLED_PLUGINS.read_text()).get("plugins", {})
    except (OSError, ValueError):
        return None
    for entries in installs.values():
        for entry in entries:
            if Path(entry.get("installPath", "/nonexistent")).resolve() == PLUGIN_ROOT:
                return entry.get("gitCommitSha", "")[:SHORT_SHA] or None
    return None


def plugin_version():
    try:
        return json.loads((PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text()).get("version", "?")
    except (OSError, ValueError):
        return "?"


@functools.lru_cache(maxsize=1)
def skills():
    return {"skills_version": plugin_version(),
            "skills_commit": commit_from_checkout() or commit_from_install() or "unknown"}
