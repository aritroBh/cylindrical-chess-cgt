#!/bin/zsh
# K26 final: generalised exact under/over search (over2.py), one heavy.sh call per shard.  PID in logs/queue_over2.pid.  Output logs/over2_*.json, queue log logs/over2/queue.log.
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo $$ > $D/logs/queue_over2.pid
for job in "cyl:8x6 2 2 1" "flat:7x6 2 2 1" "cyl:7x6 2 2 1" "cyl:8x6 3 2 2" "cyl:8x6 2 3 2" "flat:8x6 2 2 1" "flat:7x6 3 2 2" "flat:7x6 2 3 2" "cyl:7x6 3 2 2" "cyl:7x6 2 3 2" "flat:7x7 2 2 3"; do
  set -- ${=job}
  b=$1; nw=$2; nb=$3; n=$4
  for ((i=0;i<n;i++)); do
    tag=over2_${b/:/_}_$nw$nb; shard=""; [[ $n -gt 1 ]] && { tag=${tag}_s${i}of${n}; shard="--shard $i/$n"; }
    [[ -f $D/logs/$tag.json ]] && continue
    echo "start $tag $(date +%T)" >> $D/logs/over2/queue.log
    $H $PY $D/scripts/over2.py --board $b --nw $nw --nb $nb $shard > $D/logs/over2/$tag.out 2> $D/logs/over2/$tag.err
    echo "end   $tag $(date +%T) rc=$?" >> $D/logs/over2/queue.log
  done
done
echo "QUEUE DONE $(date +%T)" >> $D/logs/over2/queue.log
