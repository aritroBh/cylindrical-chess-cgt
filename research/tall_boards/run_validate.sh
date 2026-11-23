#!/bin/bash
# Validation 1 driver: for each R, 2000 random positions, python (cylcgt whole-board) vs tw.  Run from project root.
cd /Users/aritro/Downloads/Research/Chessendgames
export PYTHONPATH=$PWD
T=research/tall_boards
for R in 5 6 7 8 9 10 11 12; do
  nice -n 15 .venv/bin/python $T/validate.py $R 2000 7 7 40 $T/results/val_R$R > $T/logs/val_R$R.log 2>&1
  $T/tw --eval $T/results/val_R$R.eval > $T/results/val_R$R.c
  paste $T/results/val_R$R.c <(cut -f1 $T/results/val_R$R.py) | awk '{n++; if($1!=$2) d++} END{printf "R=%s positions=%d differences=%d\n", "'$R'", n, d+0}' >> $T/results/validation1.txt
  echo "R=$R done $(date +%T)" >> $T/logs/progress.txt
done
