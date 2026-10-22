#!/bin/sh
# Verifier A: run from the project root.  Needs kpv = cc -O2 -o kings/delegate/out/K4/verify_A/kpv kings/kpsolve.c
cd /Users/aritro/Downloads/Research/Chessendgames || exit 1
V=kings/delegate/out/K4/verify_A
[ -x $V/kpv ] || cc -O2 -o $V/kpv kings/kpsolve.c
PYTHONPATH=. nice -n 10 .venv/bin/python $V/vfacts.py > $V/facts.log 2>&1
for b in flat:3x4 cyl:3x4 flat:4x4 cyl:4x4 flat:3x5 cyl:3x5 flat:4x5 cyl:4x5 flat:5x5 cyl:5x5; do
  t=$(echo $b | tr ':' '_')
  PYTHONPATH=. nice -n 10 .venv/bin/python $V/vdriver.py $b --kp $V/kpv > $V/run_$t.log 2>&1
done
echo ALLDONE > $V/alldone.flag
