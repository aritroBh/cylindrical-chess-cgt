#!/bin/sh
# cylinder comparison (rg_copy) for the *3 question, one worker
cd "$(dirname "$0")" || exit 1
for a in "4 7" "4 8" "4 9" "5 9" "4 10"; do
  set -- $a
  ./cyl_scan.sh $1 $2 >> results/cylinder_hist.txt
  echo "$(date +%T) cylinder n=$1 P=$2 done" >> logs/progress_cyl.log
done
