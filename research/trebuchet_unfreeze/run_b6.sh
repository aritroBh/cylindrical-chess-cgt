#!/bin/zsh
# usage: run_b6.sh K  -> processes batches K, K+2, ... (chess cap1 then frozen) one at a time
cd /Users/aritro/Downloads/Research/Chessendgames/research/trebuchet_unfreeze
echo $$ > logs/b6_runner$1.pid
i=0
for f in data/b6/b_??; do
  i=$((i+1)); [ $(( (i-1) % 2 )) -eq $1 ] || continue
  b=${f:t}
  [ -s logs/b6_chess_$b.txt ] || nice -n 15 /usr/bin/time -l src/kpv --board cyl:6x6 --cap 1 --promote Q --moves < $f > logs/b6_chess_$b.tmp 2> logs/b6_chess_$b.err && mv logs/b6_chess_$b.tmp logs/b6_chess_$b.txt
  [ -s logs/b6_frozen_$b.txt ] || nice -n 15 src/kpv --board cyl:6x6 --frozen --promote Q --moves < $f > logs/b6_frozen_$b.tmp 2> logs/b6_frozen_$b.err && mv logs/b6_frozen_$b.tmp logs/b6_frozen_$b.txt
done
