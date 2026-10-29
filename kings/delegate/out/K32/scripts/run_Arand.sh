#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K32
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
for n in 5 6; do
  /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh sh -c "$PY $D/scripts/stopsA.py $n $D/data/rand$n.txt > $D/data/Arand$n.txt 2>> $D/logs/Arand.log"
  echo "rand$n done $(date +%T)" >> $D/logs/Arand.log
done
