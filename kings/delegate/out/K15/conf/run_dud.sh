#!/bin/zsh
# usage: run_dud.sh <worker 0|1>: P-model runs per (group, context), each under a 25 CPU-second limit (below the lock threshold)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15
w=$1
for g in 0 1 2 3 4 5; do
  [[ $((g%2)) -ne $w ]] && continue
  for f in conf/dud/g${g}_c*.in; do
    b=${f%.in}; [[ -s $b.out ]] && continue
    ( ulimit -t 25; nice -n 15 ./val/kpp --board cyl:8x6 --ep on --cap 1 --pmodel < $f > $b.out 2>/dev/null )
    [[ $(wc -l < $b.out) -lt 2 ]] && { rm -f $b.out; echo "$b timeout" >> conf/dud_timeouts.log; }
  done
done
echo "worker $w finished" >> conf/dud_done.log
