#!/bin/sh
# Run Lc0 on the CGT suite at the same node budgets as the Stockfish run
# (engine/runs/sf19_nodes.json). One invocation per budget, so a long 1M-node run
# cannot lose the cheaper ones. Lc0 runs with its shipped defaults (Homebrew lc0
# 0.32.1, bundled network 42850, Metal backend): in particular smart pruning may
# stop a search before the node limit once the best move is settled.
# Run from the project root:  sh engine/runs/lc0/run_lc0.sh
set -e
out=engine/runs/lc0
lc0=${LC0:-/opt/homebrew/bin/lc0}
for n in 1000 10000 100000 1000000; do
  .venv/bin/python engine/run_suite.py --engine "$lc0" \
    --epd engine/suite/cgt_verified.epd engine/suite/cgt_disagree.epd \
    --nodes "$n" --timeout 1800 --json "$out/lc0_nodes_$n.json" > "$out/lc0_nodes_$n.txt"
done
.venv/bin/python "$out/merge.py"
