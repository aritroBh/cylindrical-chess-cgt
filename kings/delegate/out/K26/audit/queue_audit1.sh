#!/bin/zsh
# K26 attempt 5: second enumerator + second solver for the one-shuttle (on / over-pre) search, <= 2+2, fresh build; starts when queue_audit.sh is done; nice 15, one shard at a time.
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo $$ > $D/logs/f/queue_audit1.pid
while ! grep -q 'AUDIT QUEUE DONE' $D/logs/f/queue_audit.log 2>/dev/null; do sleep 10; done
for b in flat:7x6 cyl:8x6 cyl:7x6; do for ((i=0;i<8;i++)); do
  tag=audit1_${b/:/_}_22_s${i}of8
  [[ -f $D/logs/f/audit/$tag.json ]] && continue
  echo "start $tag $(date +%T)" >> $D/logs/f/queue_audit1.log
  nice -n 15 $PY $D/audit/audit_t1_fresh.py --board $b --nw 2 --nb 2 --shard $i/8 > $D/logs/f/audit/run_$tag.log 2>&1
  echo "end   $tag $(date +%T) rc=$?" >> $D/logs/f/queue_audit1.log
done; done
echo "AUDIT1 QUEUE DONE $(date +%T)" >> $D/logs/f/queue_audit1.log
