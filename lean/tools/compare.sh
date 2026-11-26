#!/usr/bin/env bash
# Compare the Lean movelist with the Python printer on random positions.
# Usage (any directory): lean/tools/compare.sh [SEED] [N]     defaults: SEED=1, N=5000
# Writes lean/tools/out/positions_seedSEED.txt, lean_seedSEED.txt, py_seedSEED.txt and prints the summary.
# Needs the built binary lean/.lake/build/bin/movelist (this script does not build it).
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$ROOT/lean/tools/out"
SEED="${1:-1}"
N="${2:-5000}"
LEAN_BIN="$ROOT/lean/.lake/build/bin/movelist"
PY="$ROOT/.venv/bin/python"
IN="$OUT/positions_seed$SEED.txt"
LEAN_OUT="$OUT/lean_seed$SEED.txt"
PY_OUT="$OUT/py_seed$SEED.txt"
mkdir -p "$OUT"

nice -n 15 "$PY" "$ROOT/lean/tools/gen_positions.py" "$SEED" "$N" > "$IN"
nice -n 15 "$LEAN_BIN" < "$IN" > "$LEAN_OUT"
nice -n 15 "$PY" "$ROOT/lean/tools/py_movelist.py" < "$IN" > "$PY_OUT"

echo "input lines: $(wc -l < "$IN"), lean output lines: $(wc -l < "$LEAN_OUT"), python output lines: $(wc -l < "$PY_OUT")"
echo "positions per topology:"
awk '{n[$1]++} END {for (t in n) print "  " t ": " n[t]}' "$IN" | sort

paste -d '\t' "$IN" "$LEAN_OUT" "$PY_OUT" | awk -F'\t' '
  { split($1, a, " "); topo = a[1]; tot[topo]++
    if ($2 != $3) { bad[topo]++; nd++
      if (nd <= 10) { printf "DIFF %d (%s)\n  input: %s\n  lean:  %s\n  py:    %s\n", NR, topo, $1, $2, $3 } } }
  END {
    printf "differing lines: %d of %d\n", nd + 0, NR
    for (t in tot) printf "  %s: %d differ of %d\n", t, bad[t] + 0, tot[t]
  }'

# Named positions of the paper (lean/tools/paper_positions.txt): both printers, same setting per line.
PAPER="$ROOT/lean/tools/paper_positions.txt"
PIN="$OUT/paper_inputs.txt"
grep -v '^[[:space:]]*\(#\|$\)' "$PAPER" > "$PIN"
nice -n 15 "$LEAN_BIN" < "$PIN" > "$OUT/paper_lean.txt"
nice -n 15 "$PY" "$ROOT/lean/tools/py_movelist.py" < "$PIN" > "$OUT/paper_py.txt"
paste -d '\t' "$PIN" "$OUT/paper_lean.txt" "$OUT/paper_py.txt" | awk -F'\t' '
  $2 != $3 { n++; printf "PAPER DIFF\n  input: %s\n  lean:  %s\n  py:    %s\n", $1, $2, $3 }
  END { printf "paper positions: %d, differing: %d\n", NR, n + 0 }'
