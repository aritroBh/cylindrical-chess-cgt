#!/bin/zsh
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo "start ctx_over_0 $(date +%T)" >> $D/logs/queue9.log
$H $PY $D/scripts/ctxtest.py logs/groups_over_0.json logs/ctx_over_0.json --nbase 60 --nflip 20 --ncheck 12 > logs/ctx_over_0.log 2>&1
echo "end   ctx_over_0 $(date +%T) rc=$?" >> $D/logs/queue9.log
