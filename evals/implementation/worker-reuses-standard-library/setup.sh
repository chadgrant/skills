#!/usr/bin/env bash
set -euo pipefail
git init -q
mkdir -p src
cat > package.json <<'EOF'
{ "name": "fixture", "version": "1.0.0", "type": "module", "scripts": { "test": "node --test" } }
EOF
cat > src/clock.js <<'EOF'
export function now() { return new Date(); }
EOF
git add -A && git -c user.email=e@x -c user.name=eval commit -qm init
