#!/bin/zsh
# exact-chess kpsolve (cap 1, bounds A B) one file at a time, each under a 55 CPU-second limit (below the lock threshold)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15
for f in chess/ZB_alone.in chess/ZB_C*.in; do
  b=${f%.in}; [[ -s $b.out ]] && continue
  ( ulimit -t 55; /usr/bin/time -l nice -n 15 ./kp --board cyl:8x6 --cap 1 --threads 1 < $f > $b.out 2> $b.err )
  [[ $(wc -l < $b.out) -lt $(wc -l < $f) ]] && { echo "$b timeout" >> chess/timeouts.log; rm -f $b.out; }
done
echo finished >> chess/done.log
