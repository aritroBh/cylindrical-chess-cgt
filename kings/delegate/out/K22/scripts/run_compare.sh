#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
cd $D
for args in "flat 4 5 0 3 1 2 2 150 1 ep" "flat 4 5 0 3 1 2 2 150 2 safe" "cyl 4 6 0 3 1 2 2 150 3 ep" "flat 5 6 0 4 2 2 2 150 4 ep" "flat 5 6 0 4 2 2 2 100 5 safe ep" "cyl 7 6 0 2 2 2 2 100 6 ep"; do
  echo "== compare $args" >> logs/compare_log.txt
  $H $PY scripts/compare.py ${=args} >> logs/compare_log.txt 2>&1
done
echo ALLDONE >> logs/compare_log.txt
