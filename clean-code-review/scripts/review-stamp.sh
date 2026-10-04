#!/usr/bin/env bash
# Reads and writes the full-review stamp in a repo's AGENTS.md.
#
#   review-stamp.sh status   prints "fresh: ..." or "stale: ..." for the repo in the current directory
#   review-stamp.sh stamp    records today's date and HEAD as the last full review
#
# Limits come from REVIEW_MAX_AGE_DAYS (default 14) and REVIEW_MAX_COMMITS (default 50).
set -euo pipefail

readonly STAMP_FILE_NAME="AGENTS.md"
readonly STAMP_PREFIX="Last full review:"
readonly MAX_AGE_DAYS="${REVIEW_MAX_AGE_DAYS:-14}"
readonly MAX_COMMITS="${REVIEW_MAX_COMMITS:-50}"
readonly SECONDS_PER_DAY=86400
readonly EXIT_USAGE=2

stamp_file() {
  echo "$(git rev-parse --show-toplevel)/$STAMP_FILE_NAME"
}

stamp_line() {
  grep -m1 "^$STAMP_PREFIX" "$(stamp_file)" 2>/dev/null
}

# Stamp line: "Last full review: <YYYY-MM-DD> at commit <sha>"
stamped_date() {
  awk '{ print $4 }' <<<"$1"
}

stamped_commit() {
  awk '{ print $7 }' <<<"$1"
}

epoch_of_date() {
  date -u -d "$1" +%s 2>/dev/null || date -u -j -f "%Y-%m-%d" "$1" +%s
}

days_since() {
  echo $(( ($(date -u +%s) - $(epoch_of_date "$1")) / SECONDS_PER_DAY ))
}

commit_exists() {
  git cat-file -e "$1^{commit}" 2>/dev/null
}

report_status() {
  local line commit commits days
  if ! line="$(stamp_line)"; then
    echo "stale: no full review recorded in $STAMP_FILE_NAME"
    return
  fi
  commit="$(stamped_commit "$line")"
  if ! commit_exists "$commit"; then
    echo "stale: reviewed commit $commit is not in this repository's history"
    return
  fi
  commits="$(git rev-list --count "$commit..HEAD")"
  days="$(days_since "$(stamped_date "$line")")"
  if (( commits >= MAX_COMMITS )); then
    echo "stale: $commits commits since the last full review (limit $MAX_COMMITS)"
  elif (( days >= MAX_AGE_DAYS )); then
    echo "stale: $days days since the last full review (limit $MAX_AGE_DAYS)"
  else
    echo "fresh: $commits commits and $days days since the last full review at $commit"
  fi
}

replace_stamp_line() {
  local file="$1" new_line="$2" rewritten
  rewritten="$(mktemp)"
  awk -v prefix="$STAMP_PREFIX" -v line="$new_line" \
    'index($0, prefix) == 1 { print line; next } { print }' "$file" >"$rewritten"
  mv "$rewritten" "$file"
}

append_stamp_section() {
  local file="$1" new_line="$2"
  cat >>"$file" <<EOF

## Code review

$new_line

Stale after $MAX_AGE_DAYS days or $MAX_COMMITS commits. When stale, run the \`clean-code-review\` skill over the whole codebase; it rewrites the line above.
EOF
}

write_stamp() {
  local file new_line
  file="$(stamp_file)"
  new_line="$STAMP_PREFIX $(date -u +%Y-%m-%d) at commit $(git rev-parse HEAD)"
  if stamp_line >/dev/null; then
    replace_stamp_line "$file" "$new_line"
  else
    append_stamp_section "$file" "$new_line"
  fi
  echo "$new_line"
}

case "${1:-}" in
  status) report_status ;;
  stamp) write_stamp ;;
  *)
    echo "usage: review-stamp.sh status|stamp" >&2
    exit "$EXIT_USAGE"
    ;;
esac
