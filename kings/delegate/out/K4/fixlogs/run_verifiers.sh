#!/bin/sh
# Fix-round re-runs of the verifiers' own scripts (verify_A in place: read-only scripts; verify_B as a copy in vB_rerun/,
# because its scripts write work files).  One python process at a time, nice 10.  Logs in fixlogs/.
cd /Users/aritro/Downloads/Research/Chessendgames || exit 1
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
K4=kings/delegate/out/K4
L=$K4/fixlogs
ALL="flat:3x4 cyl:3x4 flat:4x4 cyl:4x4 flat:3x5 cyl:3x5 flat:4x5 cyl:4x5 flat:5x5 cyl:5x5"
: > $L/vA_nodecheck.log; : > $L/vA_tempo.log
for b in $ALL; do nice -n 10 .venv/bin/python $K4/verify_A/nodecheck.py $b >> $L/vA_nodecheck.log 2>&1; done
nice -n 10 .venv/bin/python $K4/vB_rerun/v_run.py $ALL > $L/vB_run.log 2>&1
nice -n 10 .venv/bin/python $K4/vB_rerun/v_check1.py $K4/vB_rerun/kp $ALL > $L/vB_check1.log 2>&1
nice -n 10 .venv/bin/python $K4/vB_rerun/v_legal.py $K4/vB_rerun/kp $ALL > $L/vB_legal.log 2>&1
nice -n 10 .venv/bin/python $K4/vB_rerun/v_bisim.py > $L/vB_bisim.log 2>&1
nice -n 10 .venv/bin/python $K4/vB_rerun/v_tempo.py $ALL > $L/vB_tempo.log 2>&1
nice -n 10 .venv/bin/python $K4/vB_rerun/v_offclass.py $ALL > $L/vB_offclass.log 2>&1
nice -n 10 .venv/bin/python $K4/vB_rerun/v_diffstats.py > $L/vB_diffstats.log 2>&1
for b in $ALL; do nice -n 10 .venv/bin/python $K4/verify_A/vtempo.py $b 10 >> $L/vA_tempo.log 2>&1; done
nice -n 10 .venv/bin/python $K4/verify_A/vfacts.py > $L/vA_facts.log 2>&1
echo done > $L/verifiers.done
