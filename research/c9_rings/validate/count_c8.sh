#!/bin/bash
# C8 root-ring counts with enum_rings --count, one process at a time under nice 15
cd "$(dirname "$0")"
for s in "9 1 8" "9 2 7" "9 3 6" "9 4 5" "10 1 9" "10 2 8" "10 3 7" "10 4 6" "10 5 5"; do
  set -- $s
  start=$(date +%s)
  r=$(nice -n 15 ./enum_rings_v 8 $1 $2 $3 --count 2>/dev/null | tail -1)
  end=$(date +%s)
  echo "8 $1 $2 $3 $r wall_s=$((end-start))" >> c8_counts.txt
done
echo ALLDONE >> c8_counts.txt
