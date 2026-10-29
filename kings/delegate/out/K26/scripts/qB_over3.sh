#!/bin/zsh
# K26 final attempt, queue B: exact under/over (U1)-(U4) with the king-freeze filter (over3.py), private build bin_r.  One heavy.sh call per shard. PID in logs/qB.pid.
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames K26_BIN=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/bin_r
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo $$ > $D/logs/qB.pid
for job in "cyl:8x6 3 2 1 3" "cyl:8x6 2 3 1 3" "cyl:8x6 2 2 3 4"; do
  set -- ${=job}
  b=$1; nw=$2; nb=$3; n=$4; nf=$5
  for ((i=0;i<n;i++)); do
    tag=over3_${b/:/_}_$nw${nb}; [[ $nf != 3 ]] && tag=${tag}_nf$nf
    shard=(); [[ $n -gt 1 ]] && { tag=${tag}_s${i}of${n}; shard=(--shard $i/$n); }
    [[ -f $D/logs/$tag.json ]] && continue
    echo "start $tag $(date +%T)" >> $D/logs/o3/queue.log
    $H $PY $D/scripts/over3.py --board $b --nw $nw --nb $nb --nf $nf $shard --tag $tag > $D/logs/o3/$tag.out 2> $D/logs/o3/$tag.err
    echo "end   $tag $(date +%T) rc=$?" >> $D/logs/o3/queue.log
  done
done
echo "QUEUE DONE $(date +%T)" >> $D/logs/o3/queue.log
