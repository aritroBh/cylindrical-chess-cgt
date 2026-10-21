#!/bin/sh
# usage: bg.sh tb|ea <log> <python args...>   (runs python -m ... in the textbook or e.p.-aware tree)
R=/Users/aritro/Downloads/Research/Chessendgames
EP=/private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt
conv=$1; log=$2; shift 2
if [ "$conv" = "ea" ]; then
  cd "$EP" && PYTHONPATH="$EP:$R" exec "$R/.venv/bin/python" "$@" > "$log" 2>&1
else
  cd "$R" && PYTHONPATH="$R" exec "$R/.venv/bin/python" "$@" > "$log" 2>&1
fi
