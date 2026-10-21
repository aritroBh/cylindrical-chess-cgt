#!/bin/sh
# verifier C3-refute: all 26,000 rows, own solver, CPU cap 30 s per side-to-move search
cd "$(dirname "$0")"
PY=../../../.venv/bin/python
for mr in "0 0" "1 0" "2 0" "0 1" "0 2" "1 1" "1 2"; do
  set -- $mr
  $PY drive.py $1 $2 30 5 res_mode$1_rule$2.txt > sum_mode$1_rule$2.json 2>&1
done
echo ALLDONE
