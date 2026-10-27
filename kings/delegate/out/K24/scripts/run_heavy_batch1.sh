#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K24
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
cd $D
for spec in "cyl:5x6 600 11" "flat:5x6 600 12" "cyl:5x5 800 13"; do
  set -- ${=spec}
  $PY scripts/soundness_bbbw.py $1 $2 $3 >> logs/soundness_bbbw.log 2>&1
done
echo done >> logs/soundness_bbbw.log
