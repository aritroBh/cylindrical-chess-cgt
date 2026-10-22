#!/bin/sh
# K8v: asymmetric stalemate rules (all 17 boards).  nohup sh kings/delegate/out/K8v/run_asym8.sh > kings/delegate/out/K8v/logs/driver3.log 2>&1 &
cd /Users/aritro/Downloads/Research/Chessendgames || exit 1
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
V=kings/delegate/out/K8v
L=$V/logs
PY=.venv/bin/python
run() { lab=$1; shift; nice -n 10 $PY $V/v6_lim.py "$lab" 3000 1200 -- nice -n 10 $PY "$@"; }
ALL17="flat:3x4 flat:4x4 cyl:4x4 cyl:3x6 cyl:2x6 cyl:2x8 cyl:3x7 cyl:3x8 flat:3x7 cyl:4x6 flat:4x6 cyl:4x7 cyl:4x8 cyl:6x5 flat:5x6 cyl:5x6 cyl:7x5"
: > $L/v8_asym.log
for b in $ALL17; do
  run "v8_asym $b" $V/v8_chess.py --asym-only $b >> $L/v8_asym.log 2>&1
  echo "asym $b done $(date +%T)"
done
echo asym-done
