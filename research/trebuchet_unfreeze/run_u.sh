#!/bin/zsh
# usage: run_u.sh K -> cap-2 resolution of cap-1-unresolved positions; batches K, K+2, ... (B first, then main)
cd /Users/aritro/Downloads/Research/Chessendgames/research/trebuchet_unfreeze
echo $$ > logs/u_runner$1.pid
i=0
for f in data/u/uB_??.txt data/u/u6_??.txt; do
  i=$((i+1)); [ $(( (i-1) % 2 )) -eq $1 ] || continue
  b=${f:t:r}
  [ -s logs/c2_$b.txt ] || nice -n 15 /usr/bin/time -l src/kpv --board cyl:6x6 --cap 2 --promote Q --moves < $f > logs/c2_$b.tmp 2> logs/c2_$b.err && mv logs/c2_$b.tmp logs/c2_$b.txt
done
