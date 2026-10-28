#!/bin/bash
# count the C9 root rings for 11 pawns, one split after the other (one process), under nice 15
cd "$(dirname "$0")"
for s in "1 10" "2 9" "3 8" "4 7" "5 6"; do
  set -- $s
  start=$(date +%s)
  r=$(nice -n 15 ./enum_rings 9 11 $1 $2 --count 2>/dev/null | tail -1)
  end=$(date +%s)
  echo "9 11 $1 $2 $r wall_s=$((end-start))"
done
