#!/bin/zsh
# K26 attempt 5, fresh reproduction with the binaries rebuilt in K26/bin (tag prefix k26f_). One heavy.sh call per shard. Usage: queueF.sh <name> "<job>" ...  job = "board nw nb type nshards"
export K26_COLLAPSE_PROMO=1 PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
name=$1; shift
echo $$ > $D/logs/f/queue_c$name.pid
for job in "$@"; do
  set -- ${=job}
  b=$1; nw=$2; nb=$3; t=$4; n=$5
  tm=12; [[ $t == t1 ]] && tm=4
  for ((i=0;i<n;i++)); do
    tag=k26c_${b/:/_}_$nw${nb}_$t
    shard=(); sfx=""
    if [[ $n -gt 1 ]]; then shard=(--shard $i/$n); sfx="_s${i}of${n}"; fi
    [[ -f $D/logs/${tag}${sfx}_summary.json ]] && continue
    echo "start $tag $i/$n $(date +%T)" >> $D/logs/f/queue_c$name.log
    /usr/bin/time -p $H $PY $D/scripts/search.py --board $b --nw $nw --nb $nb --type $t --tmax $tm $shard --tag $tag > $D/logs/f/${tag}_$i.out 2> $D/logs/f/${tag}_$i.err
    echo "end   $tag $i/$n $(date +%T) rc=$?" >> $D/logs/f/queue_c$name.log
  done
done
echo "QUEUE $name DONE $(date +%T)" >> $D/logs/f/queue_c$name.log
