#!/bin/zsh
# Sequential queue; every process is one shard of at most about 1M candidates (under one CPU-minute), nice 15.
# usage: queue2.sh "<board> <nw> <nb> <type> <nshards>" ...
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26
while [[ -z $(ls $D/logs/flat_7x6_23_t2_s0of2_summary.json 2>/dev/null) ]]; do sleep 5; done
for job in "$@"; do
  set -- ${=job}
  b=$1; nw=$2; nb=$3; t=$4; n=$5
  tm=12; [[ $t == t1 ]] && tm=4
  for ((i=0;i<n;i++)); do
    tag=${b/:/_}_$nw${nb}_$t; [[ $n -gt 1 ]] && tag=${tag}_s${i}of${n}
    if [[ -f $D/logs/${tag}_summary.json ]]; then continue; fi
    echo "start $tag $(date +%T)" >> $D/logs/queue3.log
    /usr/bin/time -p $PY $D/scripts/search.py --board $b --nw $nw --nb $nb --type $t --tmax $tm --shard $i/$n > $D/logs/run_$tag.log 2> $D/logs/time_$tag.txt
    echo "end   $tag $(date +%T) rc=$? $(tail -3 $D/logs/time_$tag.txt | tr '\n' ' ')" >> $D/logs/queue3.log
  done
done
echo "QUEUE DONE $(date +%T)" >> $D/logs/queue3.log
