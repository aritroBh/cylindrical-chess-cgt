#!/bin/zsh
# run implementation A on the six chunks of the N=4 class list, one heavy.sh call per chunk
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K32
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
for p in 00 01 02 03 04 05; do
  echo "chunk $p start $(date +%T) driver pid $$" >> $D/logs/A4.log
  /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh sh -c "$PY $D/scripts/stopsA.py 4 $D/data/c4_part_$p > $D/data/A4_part_$p.txt 2>> $D/logs/A4.log"
  echo "chunk $p done $(date +%T)" >> $D/logs/A4.log
done
