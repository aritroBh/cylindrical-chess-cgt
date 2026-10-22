#!/bin/sh
# K8v: independent check of K8, task 1 (normal play).  Run from anywhere:
#   nohup sh kings/delegate/out/K8v/run_verify8.sh > kings/delegate/out/K8v/logs/driver.log 2>&1 &
# One python process at a time, nice 10, 3 GB tree limit (v6_lim.py stops only its own child), 20 min per step.
cd /Users/aritro/Downloads/Research/Chessendgames || exit 1
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
V=kings/delegate/out/K8v
L=$V/logs
mkdir -p $L $V/work $V/out
BOARDS="${BOARDS:-cyl:5x4 cyl:3x7 cyl:2x6 cyl:2x8 cyl:3x8 flat:3x7 cyl:4x7 flat:4x6 cyl:4x8 cyl:5x7 cyl:6x7}"
PY=.venv/bin/python
run() { # label script args...
  lab=$1; shift
  nice -n 10 $PY $V/v6_lim.py "$lab" 3000 1200 -- nice -n 10 $PY "$@"
}
: > $L/v_run.log; : > $L/v_check1.log; : > $L/v6_detail.log; : > $L/v_tempo.log; : > $L/v_stale.log
: > $L/v_legal.log; : > $L/v_offclass.log
for b in $BOARDS; do
  run "v_run $b"      $V/v_run.py $b           >> $L/v_run.log 2>&1
  run "v_check1 $b"   $V/v_check1.py $V/kp $b  >> $L/v_check1.log 2>&1
  run "v6_detail $b"  $V/v6_detail.py $b       >> $L/v6_detail.log 2>&1
  run "v_tempo $b"    $V/v_tempo.py $b         >> $L/v_tempo.log 2>&1
  run "v_stale $b"    $V/v_stale.py $b         >> $L/v_stale.log 2>&1
  run "v_legal $b"    $V/v_legal.py $V/kp $b   >> $L/v_legal.log 2>&1
  run "v_offclass $b" $V/v_offclass.py $b      >> $L/v_offclass.log 2>&1
  echo "board $b done $(date +%T)"
done
(cd $V && nice -n 10 ../../../../.venv/bin/python v_cands.py > logs/v_cands.log 2>&1)
echo main-done
