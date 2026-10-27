#!/bin/zsh
# Python-vs-C++ comparison in chunks of well under one CPU-minute each (so no lock needed).
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
cd $D
i=0
for args in "flat 4 5 0 3 1 2 2 8 1 ep" "flat 4 5 0 3 2 2 2 8 2 safe" "cyl 4 6 0 3 1 2 2 8 3 ep" "flat 5 6 0 4 2 2 2 8 4 ep" "flat 5 6 0 4 2 2 2 8 5 safe ep" "cyl 7 6 0 2 2 2 2 8 6 ep" "cyl 7 6 0 2 0 2 2 8 7 ep" "flat 4 5 0 3 1 3 3 8 8 ep"; do
  echo "== compare $args (MAXATT=15)" >> logs/compare_log.txt
  MAXATT=15 nice -n 10 $PY scripts/compare.py ${=args} >> logs/compare_log.txt 2>&1
done
echo ALLDONE >> logs/compare_log.txt
