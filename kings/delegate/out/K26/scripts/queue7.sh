#!/bin/zsh
# K26: contexts on files e,f (instead of f,g) for the three exact duds of cyl:8x6, through the shared lock.
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo "start ctx_cyl8_ef $(date +%T)" >> $D/logs/queue7.log
$H $PY $D/scripts/ctxtest.py logs/groups_cyl8_ef.json logs/ctx_cyl8_ef.json --files ef --nbase 60 --nflip 20 --ncheck 12 > logs/ctx_cyl8_ef.log 2>&1
echo "end   ctx_cyl8_ef $(date +%T) rc=$?" >> $D/logs/queue7.log
