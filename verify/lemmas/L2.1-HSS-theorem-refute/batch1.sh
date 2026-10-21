#!/bin/sh
# Exhaustive runs, each capped at 1500 s of wall time inside exhaust.py.
cd /Users/aritro/Downloads/Research/Chessendgames/verify/lemmas/L2.1-HSS-theorem-refute
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
run() { PYTHONPATH= $PY -I exhaust.py "$@" 1500 > "out/ex_$1x$2_w$3_e$4_$5v$6.txt" 2>&1; }
# lane = $1
case "$1" in
  A) for w in 0 1; do for e in 0 1; do run 5 6 $w $e 3 3; done; done ;;
  B) for w in 0 1; do for e in 0 1; do run 6 6 $w $e 3 3; done; done ;;
  C) for w in 0 1; do for e in 0 1; do run 4 7 $w $e 3 3; run 6 5 $w $e 3 3; done; done ;;
  D) for w in 0 1; do for e in 0 1; do run 7 6 $w $e 3 2; run 7 6 $w $e 2 3; done; done ;;
esac
echo "lane $1 finished" > out/lane_$1.done
