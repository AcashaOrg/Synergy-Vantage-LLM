#!/usr/bin/env bash
# convert_and_commit_diagram.sh
# Convert Mermaid diagram to SVG and commit to repo.
set -euo pipefail

MERMAID_SRC="docs/diagrams/digital_epiphanies_flow.mmd"
SVG_OUT="docs/diagrams/digital_epiphanies_flow.svg"

# 1. Install Mermaid CLI if missing
if ! command -v mmdc >/dev/null 2>&1; then
  npm install -g @mermaid-js/mermaid-cli
fi

# 2. Convert .mmd to .svg with width 1024
mmdc -i "$MERMAID_SRC" -o "$SVG_OUT" -w 1024

# 3. Embed diagram in README if not already present
if ! grep -q "${SVG_OUT}" README.md; then
  printf '\n![Digital Epiphanies Flow](%s)\n' "$SVG_OUT" >> README.md
fi

# 4. Git add, commit, and push
git add "$SVG_OUT" README.md
git commit -m "Add SVG export for Digital Epiphanies Flow"
# Uncomment the next line to push automatically
# git push
