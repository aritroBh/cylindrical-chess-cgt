#!/bin/sh
# K6 independent verification (verifier B pipeline copied from K4/vB_rerun). Run from the project root:
#   nohup sh kings/delegate/out/K6/verify/run_verify6.sh > kings/delegate/out/K6/verify/logs/driver.log 2>&1 &
# One python process at a time, nice 10, 3 GB tree limit (v6_lim.py stops only its own child), 25 min per step.
cd /Users/aritro/Downloads/Research/Chessendgames || exit 1
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
V=kings/delegate/out/K6/verify
L=$V/logs
mkdir -p $L $V/work $V/out
BOARDS="${BOARDS:-cyl:6x4 cyl:7x4 cyl:8x4 cyl:3x6 cyl:6x5 cyl:7x5 cyl:8x5 cyl:4x6 cyl:5x6 flat:6x4 flat:7x4 flat:6x5 flat:7x5 flat:3x6 flat:5x6 cyl:7x6 cyl:6x6}"
PY=.venv/bin/python
run() { # label script args...
  lab=$1; shift
  nice -n 10 $PY $V/v6_lim.py "$lab" 3000 1500 -- nice -n 10 $PY "$@"
}
: > $L/v_run.log; : > $L/v_check1.log; : > $L/v6_detail.log; : > $L/v_tempo.log; : > $L/v_stale.log
for b in $BOARDS; do
  run "v_run $b"     $V/v_run.py $b           >> $L/v_run.log 2>&1
  run "v_check1 $b"  $V/v_check1.py $V/kp $b  >> $L/v_check1.log 2>&1
  run "v6_detail $b" $V/v6_detail.py $b       >> $L/v6_detail.log 2>&1
  run "v_tempo $b"   $V/v_tempo.py $b         >> $L/v_tempo.log 2>&1
  run "v_stale $b"   $V/v_stale.py $b         >> $L/v_stale.log 2>&1
  echo "board $b done $(date +%T)"
done
echo main-done
