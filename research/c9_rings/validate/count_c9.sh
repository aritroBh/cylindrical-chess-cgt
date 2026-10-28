#!/bin/bash
# C9 10-pawn root-ring counts with the shipped enum_rings (default, --general, --check), one process at a time, nice 15
cd "$(dirname "$0")"
E=../enum_rings
: > c9_counts.txt
for s in "1 9" "2 8" "3 7" "4 6" "5 5" "6 4" "7 3" "8 2" "9 1"; do
  set -- $s
  st=$(date +%s); r=$(nice -n 15 $E 9 10 $1 $2 --count 2>/dev/null | tail -1); en=$(date +%s)
  echo "default 9 10 $1 $2 $r wall_s=$((en-st))" >> c9_counts.txt
done
for s in "3 7" "4 6" "5 5"; do
  set -- $s
  st=$(date +%s); r=$(nice -n 15 $E 9 10 $1 $2 --count --general 2>/dev/null | tail -1); en=$(date +%s)
  echo "general 9 10 $1 $2 $r wall_s=$((en-st))" >> c9_counts.txt
done
for s in "3 7" "4 6" "5 5"; do
  set -- $s
  st=$(date +%s); r=$(nice -n 15 $E 9 10 $1 $2 --count --check 2>/dev/null | tail -1); en=$(date +%s)
  echo "check 9 10 $1 $2 $r wall_s=$((en-st))" >> c9_counts.txt
done
echo ALLDONE >> c9_counts.txt
