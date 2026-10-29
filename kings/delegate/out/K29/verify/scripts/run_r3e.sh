#!/bin/zsh
# run_r3e.sh: flat configurations only (second run; board syntax flat7x6 for ref3); the cyl configurations were run first with the same script
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/verify
while read name board zs fz; do
  ( time nice -n 15 ./bin/ref3enum --board $board --zs $zs --fz $fz > data/r3e_$name.txt ) 2> logs/r3e_$name.time
  echo "$name $(wc -l < data/r3e_$name.txt) $(head -1 logs/r3e_$name.time)"
done <<L
flat7x6_f3_z0 flat7x6 0 3
flat7x6_f4_z0 flat7x6 0 4
flat7x6_f3_z2 flat7x6 2 3
flat8x6_f3_z0 flat8x6 0 3
flat8x6_f4_z0 flat8x6 0 4
flat8x6_f3_z2 flat8x6 2 3
L
