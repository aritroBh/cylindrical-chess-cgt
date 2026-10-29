#!/bin/zsh
# K26 final: context top-up (>= 60 contexts) for the exact groups whose first run had 59.  One heavy.sh call per group.  PID in logs/queue_topup.pid.
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo $$ > $D/logs/queue_topup.pid
for f in $D/logs/topup/g_*.json; do
  b=${f:t:r}
  [[ -f $D/logs/topup/ctx_${b#g_}.json ]] && continue
  echo "start $b $(date +%T)" >> $D/logs/topup/queue.log
  $H $PY $D/scripts/ctxtest.py $f $D/logs/topup/ctx_${b#g_}.json --nbase 66 --nflip 6 --ncheck 12 --seed 2 > $D/logs/topup/ctx_${b#g_}.log 2>&1
  echo "end   $b $(date +%T) rc=$?" >> $D/logs/topup/queue.log
done
echo "QUEUE DONE $(date +%T)" >> $D/logs/topup/queue.log
