#!/bin/zsh
# K65 referee: ax65 with the ladders T_0..T_lmax on groups from a list; stops at logs/STOP.
cd "$(dirname $0)/.."
list=$1; shift
while IFS='|' read nm pcs z0 z1; do
  [[ -f logs/STOP ]] && { echo "STOP: chain halted before $nm"; exit 1; }
  zsh src/run.sh lad/$nm bin/ax65 flat:8x8 "$pcs" $z0 $z1 "$@"
  echo "$nm $(cat logs/lad/$nm.rc)"; grep -E '^LADDER|stable' logs/lad/$nm.out
done < $list
