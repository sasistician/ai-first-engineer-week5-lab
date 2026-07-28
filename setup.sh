#!/usr/bin/env bash
# Check-and-guide setup for the Week 5 squad lab. Never installs anything
# silently — every failure prints the exact command to run, then exits so you
# can re-run this script once it's done.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEEK3_LAB="$HERE/../week3-lab"

fail() {
    echo "✗ $1"
    echo "  → $2"
    exit 1
}

echo "Checking Week 5 squad lab prerequisites..."

[ -d "$WEEK3_LAB" ] || fail \
    "../week3-lab not found next to this repo" \
    "Clone/keep EVBot (Week 3) as a sibling directory: git clone https://github.com/sasistician/evbot-week3-lab.git ../week3-lab"

[ -d "$WEEK3_LAB/.venv" ] || fail \
    "../week3-lab exists but hasn't been set up yet" \
    "cd ../week3-lab && ./setup.sh"

command -v claude >/dev/null 2>&1 || fail \
    "Claude Code CLI not found on PATH" \
    "Install Claude Code first — see https://docs.claude.com/claude-code"

command -v uv >/dev/null 2>&1 || fail \
    "uv not found on PATH" \
    "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"

echo "✓ ../week3-lab (EVBot) is set up"
echo "✓ claude CLI found"
echo "✓ uv found"
echo
echo "All set. Next: open LAB_GUIDE.md (in this repo) and start with Step 1."
