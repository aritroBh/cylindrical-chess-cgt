#!/bin/zsh
# usage: run_pm2.sh <worker 0|1> ; processes conf/pm_todo.txt lines i%2==worker, each under a 40 CPU-second limit
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15
w=$1; i=0
while read f; do
  i=$((i+1)); [[ $((i%2)) -ne $w ]] && continue
  b=${f%.in}; [[ -s $b.out ]] && continue
  ( ulimit -t 40; nice -n 15 ./val/kpp --board cyl:8x6 --ep on --cap 1 --pmodel < $f > $b.out 2>/dev/null )
  n=$(wc -l < $b.out); m=$(wc -l < $f)
  [[ $n -lt $m ]] && { echo "$b incomplete ($n/$m)" >> conf/pm_incomplete.log; rm -f $b.out; }
done < conf/pm_todo.txt
echo "worker $w finished" >> conf/pm_done.log
