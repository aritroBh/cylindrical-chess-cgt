#!/bin/zsh
# K26 attempt 5: the referee's own two-shuttle search (own enumerator, ref3m only) for flat 7x7, 2+2, 8 shards, each through heavy.sh. Output logs/f/audit/my7x7_*.json
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
cd $D
echo $$ > $D/logs/f/queue_my7x7.pid
for ((i=0;i<8;i++)); do
  o=$D/logs/f/audit/my7x7_22_s${i}of8.json
  [[ -f $o ]] && continue
  echo "start my7x7 $i/8 $(date +%T)" >> $D/logs/f/queue_my7x7.log
  $H $PY $D/audit/my_t2_fresh.py flat7x7 2 2 $o $i/8 2> $D/logs/f/audit/my7x7_22_s${i}of8.err
  echo "end   my7x7 $i/8 $(date +%T) rc=$?" >> $D/logs/f/queue_my7x7.log
done
echo "MY7X7 DONE $(date +%T)" >> $D/logs/f/queue_my7x7.log
