#!/bin/zsh
# K26 audit queue: second enumerator (enum2.py) + second solver (ref3m) on the two-shuttle search, <= 2+2 pawns; every shard < 1 CPU-minute, nice 15.
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
for b in flat:7x6 cyl:8x6 cyl:7x6 flat:8x6; do for ((i=0;i<6;i++)); do
  tag=audit_${b/:/_}_22_s${i}of6
  [[ -f $D/logs/$tag.json ]] && continue
  echo "start $tag $(date +%T)" >> $D/logs/queue6.log
  nice -n 15 $PY $D/scripts/audit_s1.py --board $b --nw 2 --nb 2 --shard $i/6 > $D/logs/run_$tag.log 2>&1
  echo "end   $tag $(date +%T) rc=$?" >> $D/logs/queue6.log
done; done
echo "QUEUE6 DONE $(date +%T)" >> $D/logs/queue6.log
