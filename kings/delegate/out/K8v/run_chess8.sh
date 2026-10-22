#!/bin/sh
# K8v: independent check of K8, task 2 (chess stalemate rule), asymmetric rules and mask tests.  Run from anywhere:
#   nohup sh kings/delegate/out/K8v/run_chess8.sh > kings/delegate/out/K8v/logs/driver2.log 2>&1 &
# One python process at a time, nice 10, 3 GB tree limit, 20 min per step.
cd /Users/aritro/Downloads/Research/Chessendgames || exit 1
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
V=kings/delegate/out/K8v
L=$V/logs
PY=.venv/bin/python
run() { lab=$1; shift; nice -n 10 $PY $V/v6_lim.py "$lab" 3000 1200 -- nice -n 10 $PY "$@"; }
CHESS="flat:3x4 flat:4x4 cyl:4x4 cyl:3x6 cyl:2x6 cyl:2x8 cyl:3x7 cyl:3x8 cyl:4x6 cyl:6x5 flat:5x6 cyl:5x6 cyl:7x5"
ALL17="flat:3x4 flat:4x4 cyl:4x4 cyl:3x6 cyl:2x6 cyl:2x8 cyl:3x7 cyl:3x8 flat:3x7 cyl:4x6 flat:4x6 cyl:4x7 cyl:4x8 cyl:6x5 flat:5x6 cyl:5x6 cyl:7x5"
: > $L/v8_chess.log; : > $L/v8_asym.log; : > $L/v8_mask.log
for b in $CHESS; do
  run "v8_chess $b" $V/v8_chess.py $b >> $L/v8_chess.log 2>&1
  echo "chess $b done $(date +%T)"
done
for b in $ALL17; do
  run "v8_asym $b" $V/v8_chess.py --asym-only $b >> $L/v8_asym.log 2>&1
  echo "asym $b done $(date +%T)"
done
for b in $ALL17; do
  run "v8_mask $b" $V/v8_mask.py $b >> $L/v8_mask.log 2>&1
  echo "mask $b done $(date +%T)"
done
echo chess-done
