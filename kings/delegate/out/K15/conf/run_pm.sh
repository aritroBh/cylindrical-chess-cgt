#!/bin/zsh
# P-model confirmation, one group (12 positions) at a time, each under a 55 CPU-second limit (below the 1 CPU-minute lock threshold)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15
for f in conf/pm/g*.in; do
  b=${f%.in}
  [[ -s $b.out ]] && continue
  ( ulimit -t 55; nice -n 15 ./val/kpp --board cyl:8x6 --ep on --cap 1 --pmodel < $f > $b.out 2>/dev/null )
  n=$(wc -l < $b.out); m=$(wc -l < $f)
  [[ $n -lt $m ]] && { echo "$b incomplete ($n/$m)" >> conf/pm_incomplete.log; rm -f $b.out; }
done
echo finished >> conf/pm_done.log
