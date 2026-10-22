#!/bin/sh
# K6 verification, part 2: legal-set check, off-class check, bisimulation of test games, graph comparison with the
# builder's graph (small boards only), candidate signatures, negative controls.  One python process at a time, nice 10.
#   nohup sh kings/delegate/out/K6/verify/run_extra6.sh > kings/delegate/out/K6/verify/logs/driver2.log 2>&1 &
cd /Users/aritro/Downloads/Research/Chessendgames || exit 1
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
V=kings/delegate/out/K6/verify
L=$V/logs
PY=.venv/bin/python
BOARDS="cyl:6x4 cyl:7x4 cyl:8x4 cyl:3x6 cyl:6x5 cyl:7x5 cyl:8x5 cyl:4x6 cyl:5x6 flat:6x4 flat:7x4 flat:6x5 flat:7x5 flat:3x6 flat:5x6 cyl:7x6 cyl:6x6"
run() { lab=$1; shift; nice -n 10 $PY $V/v6_lim.py "$lab" 3000 1500 -- nice -n 10 $PY "$@"; }
: > $L/v_legal.log; : > $L/v_offclass.log; : > $L/v_bisim.log; : > $L/v_cmp_graph.log; : > $L/v_cands.log; : > $L/v_negctl.log
for b in $BOARDS; do
  run "v_legal $b" $V/v_legal.py $V/kp $b >> $L/v_legal.log 2>&1
  run "v_offclass $b" $V/v_offclass.py $b >> $L/v_offclass.log 2>&1
  echo "extra $b done $(date +%T)"
done
run "v_bisim" $V/v_bisim.py > $L/v_bisim.log 2>&1
(cd $V && nice -n 10 ../../../../../.venv/bin/python v_cands.py > logs/v_cands.log 2>&1)
for b in cyl:3x6 flat:3x6 cyl:4x6 cyl:6x4; do
  run "v_cmp_graph $b" $V/v_cmp_graph.py $b >> $L/v_cmp_graph.log 2>&1
done
(cd $V && run_neg=1; for b in cyl:3x6 flat:3x6; do nice -n 10 ../../../../../.venv/bin/python v6_negctl.py $b >> logs/v_negctl.log 2>&1; done)
echo extra-done
