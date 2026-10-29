#!/bin/zsh
# K26 final attempt, queue C: the two-shuttle searches t2 again with promotions counted once (K26_COLLAPSE_PROMO=1), private build bin_r, tag prefix c2_.
# 2+2 on the five boards and 3+2 on flat:7x6, cyl:7x6, cyl:8x6 (2+3 is the tau-mirror of 3+2).  One heavy.sh call per shard.  PID in logs/qC.pid.
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames K26_BIN=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/bin_r K26_COLLAPSE_PROMO=1
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo $$ > $D/logs/qC.pid
for job in "flat:7x6 2 2 1" "cyl:7x6 2 2 2" "cyl:8x6 2 2 2" "flat:8x6 2 2 1" "flat:7x6 3 2 2" "cyl:7x6 3 2 4" "cyl:8x6 3 2 4" "flat:7x7 2 2 4"; do
  set -- ${=job}
  b=$1; nw=$2; nb=$3; n=$4
  for ((i=0;i<n;i++)); do
    tag=c2_${b/:/_}_$nw${nb}_t2
    shard=(); [[ $n -gt 1 ]] && shard=(--shard $i/$n)
    [[ -f $D/logs/${tag}_s${i}of${n}_summary.json || -f $D/logs/${tag}_summary.json ]] && continue
    echo "start $tag $i/$n $(date +%T)" >> $D/logs/c2/queue.log
    $H $PY $D/scripts/search.py --board $b --nw $nw --nb $nb --type t2 --tmax 12 $shard --tag $tag > $D/logs/c2/${tag}_$i.out 2> $D/logs/c2/${tag}_$i.err
    echo "end   $tag $i/$n $(date +%T) rc=$?" >> $D/logs/c2/queue.log
  done
done
echo "QUEUE DONE $(date +%T)" >> $D/logs/c2/queue.log
