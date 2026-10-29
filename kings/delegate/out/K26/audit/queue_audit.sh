#!/bin/zsh
# K26 attempt 5: the second-enumerator + second-solver audit again with the fresh build, <= 2+2, 8 shards per board; each shard about 40 CPU-s, nice 15, one at a time (no heavy.sh: under one CPU-minute each).
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo $$ > $D/logs/f/queue_audit.pid
for b in flat:7x6 cyl:8x6 cyl:7x6 flat:8x6; do for ((i=0;i<8;i++)); do
  tag=audit_${b/:/_}_22_s${i}of8
  [[ -f $D/logs/f/audit/$tag.json ]] && continue
  echo "start $tag $(date +%T)" >> $D/logs/f/queue_audit.log
  nice -n 15 $PY $D/audit/audit_s1_fresh.py --board $b --nw 2 --nb 2 --shard $i/8 > $D/logs/f/audit/run_$tag.log 2>&1
  echo "end   $tag $(date +%T) rc=$?" >> $D/logs/f/queue_audit.log
done; done
echo "AUDIT QUEUE DONE $(date +%T)" >> $D/logs/f/queue_audit.log
