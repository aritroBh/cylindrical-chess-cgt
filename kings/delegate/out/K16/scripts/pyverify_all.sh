#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
for t in cyl_6x6_20:cyl:6x6 cyl_7x6_20:cyl:7x6 cyl_8x6_20:cyl:8x6 flat_6x6_20:flat:6x6 flat_6x6_11:flat:6x6 flat_7x6_20:flat:7x6 flat_7x6_11:flat:7x6; do
  f=${t%%:*}; b=${t#*:}
  [ -s $D/work/small/$f.viol ] && nice -n 15 $PY $D/scripts/pyverify.py $b $D/work/small/$f.viol 400 | tail -2
done
