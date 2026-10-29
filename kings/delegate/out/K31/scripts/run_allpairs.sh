#!/bin/zsh
# task 3, second route: the referee's exhaustive `lk allpairs` (two-component sums of every ordered pair of B34-named roots,
# including the +1 and -1 roots, against the reference sums of the names).  Each run is well under one CPU-minute (no lock, nice 15).
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31
for spec in "cyl:6x6 a2" "cyl:6x6 a3" "cyl:6x6 a4" "cyl:8x6 a2" "cyl:8x6 a3" "cyl:8x6 a4" "cyl:8x5 a2" "cyl:8x5 a3" "cyl:10x6 a2" "cyl:10x6 a3" "cyl:10x6 a4" "cyl:6x7 a3" "cyl:7x6 a3" "cyl:9x6 a3"; do
  set -- ${=spec}
  /usr/bin/time -l nice -n 15 $D/bin/lk allpairs $1 $2 free 2> $D/logs/allpairs_tmp.time | head -3
  echo "   [$spec] $(egrep 'real|maximum resident' $D/logs/allpairs_tmp.time | tr -s ' ' | tr '\n' ' ')"
done
