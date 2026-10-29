#!/bin/zsh
# after worker A: 4-file over/on search on cyl:8x6 (<=2+2), then the 2+3 cylinder dud searches (colour mirrors of 3+2)
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
while [[ -z $(ls $D/logs/cyl_8x6_32_t2_s3of4_summary.json 2>/dev/null) ]]; do sleep 5; done
n=7
for ((i=0;i<n;i++)); do
  tag=cyl_8x6_22_t1_nf4_s${i}of${n}
  [[ -f $D/logs/${tag}_summary.json ]] && continue
  echo "start $tag $(date +%T)" >> $D/logs/queue3.log
  /usr/bin/time -p $PY $D/scripts/search.py --board cyl:8x6 --nw 2 --nb 2 --type t1 --tmax 4 --nf 4 --shard $i/$n > $D/logs/run_$tag.log 2> $D/logs/time_$tag.txt
  echo "end   $tag $(date +%T) rc=$?" >> $D/logs/queue3.log
done
for b in cyl:7x6 cyl:8x6; do for ((i=0;i<4;i++)); do
  tag=${b/:/_}_23_t2_s${i}of4
  [[ -f $D/logs/${tag}_summary.json ]] && continue
  echo "start $tag $(date +%T)" >> $D/logs/queue3.log
  /usr/bin/time -p $PY $D/scripts/search.py --board $b --nw 2 --nb 3 --type t2 --tmax 12 --shard $i/4 > $D/logs/run_$tag.log 2> $D/logs/time_$tag.txt
  echo "end   $tag $(date +%T) rc=$?" >> $D/logs/queue3.log
done; done
echo "QUEUE3C DONE $(date +%T)" >> $D/logs/queue3.log
