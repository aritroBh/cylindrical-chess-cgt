#!/bin/zsh
R=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify/r2
cd $R/data
for i in 1 2 3 4 5 6 7 8; do
  sed -n "$((2*i-1)),$((2*i))p" probe5_pos > p5_$i.pos
  /usr/bin/time -l nice -n 15 $R/bin/ref3 --board cyl:7x6 < p5_$i.pos > p5_$i.out 2> p5_$i.err
  echo "$i $(grep -E 'maximum resident|real' p5_$i.err | tr '\n' ' ') $(cat p5_$i.out | tr '\n' ';')"
done
