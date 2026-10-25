#!/usr/bin/env bash
set -euo pipefail
mkdir -p shared-state
printf 'owned by another run\n' > shared-state/keep.txt
cat > app.py <<'PYAPP'
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=["create", "fail"])
parser.add_argument("--data-dir", required=True)
parser.add_argument("--name", required=True)
args = parser.parse_args()
state = Path(args.data_dir)
state.mkdir(parents=True, exist_ok=True)
record = {"name": args.name}
if args.action == "fail":
    (state / "partial.json").write_text(json.dumps(record))
    parser.exit(3, "simulated failure after partial write\n")
(state / "record.json").write_text(json.dumps(record))
print(json.dumps({"created": record}))
PYAPP
