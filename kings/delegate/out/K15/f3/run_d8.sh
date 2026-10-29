#!/bin/zsh
# P-model confirmation of the 8x6 dud candidates in chunks, each under 58 CPU-seconds (below the one-minute lock threshold), nice 15
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/f3/cf
rm -f d8x6.out d8x6.chunk.*; split -l 480 d8x6.in d8x6.chunk.
for c in d8x6.chunk.??; do
  ( ulimit -t 58; nice -n 15 ../kpp --board cyl:8x6 --ep on --cap 0 --pmodel < $c > $c.out 2> $c.err )
  n=$(wc -l < $c.out); m=$(wc -l < $c); echo "$c $n/$m" >> d8x6.progress
done
cat d8x6.chunk.??.out > d8x6.out 2>/dev/null
echo finished >> d8x6.progress
