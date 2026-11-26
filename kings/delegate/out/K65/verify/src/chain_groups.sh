#!/bin/zsh
# K65 referee: ax65 on groups from a list (name|pieces|z0|z1), one run each through src/run.sh; stops at logs/STOP.
cd "$(dirname $0)/.."
list=$1; shift
while IFS='|' read nm pcs z0 z1; do
  [[ -f logs/STOP ]] && { echo "STOP: chain halted before $nm"; exit 1; }
  [[ -f logs/g/$nm.rc ]] && continue
  zsh src/run.sh g/$nm bin/ax65 flat:8x8 "$pcs" $z0 $z1 "$@"
  echo "$nm $(cat logs/g/$nm.rc) $(grep -E 'DEFINITION|^\(B1\)|ABORT' logs/g/$nm.out | tr '\n' ' ')"
done < $list
