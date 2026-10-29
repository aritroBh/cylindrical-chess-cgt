#!/bin/zsh
# K26 reproduction of the main searches by the final (post-reboot) attempt: same scripts, fresh binaries (byte-identical to the old ones), tag prefix repro_.
# Every process goes through the shared lock heavy.sh.  Records its own PID in logs/queue_repro.pid.
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
cd $D
echo $$ > $D/logs/queue_repro.pid
for job in "flat:7x6 2 2 t2 1" "cyl:8x6 2 2 t2 2" "cyl:7x6 2 2 t2 2" "flat:7x6 2 2 t1 1" "cyl:8x6 2 2 t1 2" "cyl:7x6 2 2 t1 2" "flat:8x6 2 2 t2 1" "flat:7x6 3 2 t2 2" "cyl:8x6 3 2 t2 4"; do
  set -- ${=job}
  b=$1; nw=$2; nb=$3; t=$4; n=$5
  tm=12; [[ $t == t1 ]] && tm=4
  for ((i=0;i<n;i++)); do
    tag=repro_${b/:/_}_$nw${nb}_$t
    shard=""; [[ $n -gt 1 ]] && shard="--shard $i/$n"
    [[ -f $D/logs/${tag}_s${i}of${n}_summary.json || -f $D/logs/${tag}_summary.json ]] && continue
    echo "start $tag $i/$n $(date +%T)" >> $D/repro/queue.log
    $H $PY $D/scripts/search.py --board $b --nw $nw --nb $nb --type $t --tmax $tm $shard --tag $tag > $D/repro/run_${tag}_$i.log 2> $D/repro/time_${tag}_$i.txt
    echo "end   $tag $i/$n $(date +%T) rc=$?" >> $D/repro/queue.log
  done
done
echo "QUEUE DONE $(date +%T)" >> $D/repro/queue.log
