#!/bin/zsh
# context test of the over_exact (one-sided zugzwang) groups, 2 groups per run, every run through the shared lock.
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
for i in 0 1 2; do
  echo "start ctx_over_$i $(date +%T)" >> $D/logs/queue4.log
  $H $PY $D/scripts/ctxtest.py logs/groups_over_$i.json logs/ctx_over_$i.json --nbase 60 --nflip 20 --ncheck 12 > logs/ctx_over_$i.log 2>&1
  echo "end   ctx_over_$i $(date +%T) rc=$?" >> $D/logs/queue4.log
done
echo "QUEUE4A DONE $(date +%T)" >> $D/logs/queue4.log
