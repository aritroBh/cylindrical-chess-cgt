#!/bin/zsh
# K26 attempt 5: exact under/over (U1)-(U4) searches (over3.py) again with the fresh build in K26/bin, tag prefix k26f_over3_. One heavy.sh call per shard.
# Usage: queueF_over.sh <name> "<board nw nb nshards nf>" ...
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
name=$1; shift
echo $$ > $D/logs/f/queue_$name.pid
for job in "$@"; do
  set -- ${=job}
  b=$1; nw=$2; nb=$3; n=$4; nf=$5
  for ((i=0;i<n;i++)); do
    tag=k26f_over3_${b/:/_}_$nw$nb; [[ $nf != 3 ]] && tag=${tag}_nf$nf
    shard=(); [[ $n -gt 1 ]] && { tag=${tag}_s${i}of${n}; shard=(--shard $i/$n); }
    [[ -f $D/logs/$tag.json ]] && continue
    echo "start $tag $(date +%T)" >> $D/logs/f/queue_$name.log
    $H $PY $D/scripts/over3.py --board $b --nw $nw --nb $nb --nf $nf $shard --tag $tag > $D/logs/f/$tag.out 2> $D/logs/f/$tag.err
    echo "end   $tag $(date +%T) rc=$?" >> $D/logs/f/queue_$name.log
  done
done
echo "QUEUE $name DONE $(date +%T)" >> $D/logs/f/queue_$name.log
