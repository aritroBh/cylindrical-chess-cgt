#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
for b in flat:6x6 flat:7x6 cyl:6x6 cyl:7x6 cyl:8x6; do
  f=$D/work/pysample_${b//:/_}.txt
  [ -s $f ] && nice -n 15 $PY $D/scripts/pyverify.py $b $f | tail -1
done
