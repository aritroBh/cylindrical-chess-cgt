#!/bin/zsh
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo $$ > $D/logs/f/queue_E3.pid
i=3
echo "start ctx_final_$i $(date +%T)" >> $D/logs/f/queue_E3.log
$H $PY $D/scripts/ctxtest.py $D/logs/f/ctx/g_final_$i.json $D/logs/f/ctx/ctx_final_$i.json --nbase 66 --nflip 6 --ncheck 12 --seed 3 > $D/logs/f/ctx/ctx_final_$i.log 2>&1
echo "QUEUE E3 DONE $(date +%T)" >> $D/logs/f/queue_E3.log
