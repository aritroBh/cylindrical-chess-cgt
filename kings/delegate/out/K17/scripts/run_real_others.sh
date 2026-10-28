#!/bin/zsh
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K17/scripts
for sp in "cyl:5x6|3|3" "flat:6x6|3,4,5|2" "cyl:7x6|3,4,5|2"; do
  IFS='|' read a b c <<< "$sp"
  echo "== $a $b $c"
  HEAVY=1 $PY search_A_real.py $a $b $c 2>&1 | grep -E "hits|rror|kpsolve"
  HEAVY=1 $PY search_A_real2.py $a 2>&1 | grep -E "hits|rror|CLEAN"
done
