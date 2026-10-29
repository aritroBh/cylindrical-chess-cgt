#!/bin/zsh
# task 3: sums of two +-1 roots (and of a +-1 root with the integer +-1) against integer contexts c = -N..N.
# each run is well under one CPU-minute (1.5 CPU-s and 660 MB for cyl:8x6 N=3), so no lock; nice 15.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31
for spec in "cyl:6x6 a2 4" "cyl:6x6 a3 4" "cyl:6x6 a4 4" "cyl:8x6 a2 3" "cyl:8x6 a3 3" "cyl:8x6 a4 3" "cyl:8x5 a2 3" "cyl:8x5 a3 3" "cyl:10x6 a2 2" "cyl:10x6 a3 2" "cyl:10x6 a4 2" "cyl:6x7 a3 3" "cyl:8x7 a4 2"; do
  set -- ${=spec}
  echo "== $spec" >> $D/logs/pairs.out
  /usr/bin/time -l nice -n 15 $D/bin/tempo pairs $1 $2 free $3 >> $D/logs/pairs.out 2> $D/logs/pairs_tmp.time
  egrep "maximum resident|user" $D/logs/pairs_tmp.time | tr '\n' ' ' >> $D/logs/pairs.out; echo >> $D/logs/pairs.out
done
echo DONE >> $D/logs/pairs.out
