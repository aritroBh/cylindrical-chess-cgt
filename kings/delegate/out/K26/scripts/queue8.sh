#!/bin/zsh
# K26 audit queue 2: second enumerator + second solver for the one-shuttle (on / over-pre) search, <= 2+2 pawns; shards < 1 CPU-minute.
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
while ! grep -q 'QUEUE6 DONE' $D/logs/queue6.log 2>/dev/null; do sleep 10; done
for b in flat:7x6 cyl:8x6 cyl:7x6; do for ((i=0;i<8;i++)); do
  tag=audit1_${b/:/_}_22_s${i}of8
  [[ -f $D/logs/$tag.json ]] && continue
  echo "start $tag $(date +%T)" >> $D/logs/queue8.log
  nice -n 15 $PY $D/scripts/audit_t1.py --board $b --nw 2 --nb 2 --shard $i/8 > $D/logs/run_$tag.log 2>&1
  echo "end   $tag $(date +%T) rc=$?" >> $D/logs/queue8.log
done; done
echo "QUEUE8 DONE $(date +%T)" >> $D/logs/queue8.log
