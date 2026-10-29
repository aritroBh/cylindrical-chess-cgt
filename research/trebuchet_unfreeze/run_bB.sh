#!/bin/zsh
# usage: run_b6.sh K  -> processes batches K, K+2, ... (chess cap1 then frozen) one at a time
cd /Users/aritro/Downloads/Research/Chessendgames/research/trebuchet_unfreeze
echo $$ > logs/bB_runner$1.pid
i=0
for f in data/bB/b_??; do
  i=$((i+1)); [ $(( (i-1) % 2 )) -eq $1 ] || continue
  b=${f:t}
  [ -s logs/bB_chess_$b.txt ] || nice -n 15 /usr/bin/time -l src/kpv --board cyl:6x6 --cap 1 --promote Q --moves < $f > logs/bB_chess_$b.tmp 2> logs/bB_chess_$b.err && mv logs/bB_chess_$b.tmp logs/bB_chess_$b.txt
  [ -s logs/bB_frozen_$b.txt ] || nice -n 15 src/kpv --board cyl:6x6 --frozen --promote Q --moves < $f > logs/bB_frozen_$b.tmp 2> logs/bB_frozen_$b.err && mv logs/bB_frozen_$b.tmp logs/bB_frozen_$b.txt
done
