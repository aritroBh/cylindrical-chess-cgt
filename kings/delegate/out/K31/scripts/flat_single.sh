#!/bin/zsh
# K31 side check: single blocked pair on FLAT boards (every file, every pair rank): number of +1 / -1 roots (referee's lk, B34 names).
# Each lk run takes under a second at these sizes (no lock needed, nice 15).
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31
for H in 5 6 7; do for W in 5 6 7 8 9 10; do for r in $(seq 2 $((H-2))); do for f in a b c d e; do
  fi=$(( $(printf '%d' "'$f") - 96 )); (( fi > (W+1)/2 )) && continue
  o=$(nice -n 15 $D/bin/lk classify flat:${W}x${H} ${f}${r} free 2>&1)
  p=$(echo "$o" | awk '$1=="+1"{print $2}'); m=$(echo "$o" | awk '$1=="-1"{print $2}')
  echo "flat:${W}x${H} ${f}${r} +1=${p:-0} -1=${m:-0}"
done; done; done; done
