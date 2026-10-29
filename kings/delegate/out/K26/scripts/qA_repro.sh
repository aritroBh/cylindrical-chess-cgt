#!/bin/zsh
# K26 final attempt, queue A: reproduction of the <= 2+2 searches with the privately rebuilt binaries (bin_r), tag prefix k26r_.  One heavy.sh call per shard. PID in logs/qA.pid.
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames K26_BIN=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/bin_r
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo $$ > $D/logs/qA.pid
for job in "cyl:7x6 2 2 t2 2" "cyl:8x6 2 2 t2 2" "cyl:7x6 2 2 t1 2" "cyl:8x6 2 2 t1 2" "flat:7x7 2 2 t2 4" "flat:7x7 2 2 t1 3"; do
  set -- ${=job}
  b=$1; nw=$2; nb=$3; t=$4; n=$5
  tm=12; [[ $t == t1 ]] && tm=4
  for ((i=0;i<n;i++)); do
    tag=k26r_${b/:/_}_$nw${nb}_$t
    shard=(); [[ $n -gt 1 ]] && shard=(--shard $i/$n)
    [[ -f $D/logs/${tag}_s${i}of${n}_summary.json || -f $D/logs/${tag}_summary.json ]] && continue
    echo "start $tag $i/$n $(date +%T)" >> $D/logs/r2/queue.log
    $H $PY $D/scripts/search.py --board $b --nw $nw --nb $nb --type $t --tmax $tm $shard --tag $tag > $D/logs/r2/${tag}_$i.out 2> $D/logs/r2/${tag}_$i.err
    echo "end   $tag $i/$n $(date +%T) rc=$?" >> $D/logs/r2/queue.log
  done
done
echo "QUEUE DONE $(date +%T)" >> $D/logs/r2/queue.log
