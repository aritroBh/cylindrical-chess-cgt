#!/bin/zsh
# K26 queue 5: cyl:7x6 and cyl:8x6, <= 2+3 pawns, one-shuttle search (type t1); each shard through the shared lock (heavy.sh).
# (queue4b did the same but crashed on os.nice under heavy.sh; fixed with safe_nice in k26lib.)
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
for b in cyl:7x6 cyl:8x6; do for ((i=0;i<3;i++)); do
  tag=${b/:/_}_23_t1_s${i}of3
  [[ -f $D/logs/${tag}_summary.json ]] && continue
  echo "start $tag $(date +%T)" >> $D/logs/queue5.log
  /usr/bin/time -p $H $PY $D/scripts/search.py --board $b --nw 2 --nb 3 --type t1 --tmax 4 --shard $i/3 > $D/logs/run_$tag.log 2> $D/logs/time_$tag.txt
  echo "end   $tag $(date +%T) rc=$?" >> $D/logs/queue5.log
done; done
echo "QUEUE5 DONE $(date +%T)" >> $D/logs/queue5.log
