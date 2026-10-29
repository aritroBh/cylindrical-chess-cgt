#!/bin/zsh
# run_enum.sh: enumerate bare P-frozen groups (P value (L,W)) with <= 2 Z-pawns a side, kings and Z-pawns on the files of F_Z.
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
while read name board zs fz; do
  ( time nice -n 15 ./bin/grp --board $board --mode enum --zs $zs --fz $fz --zw 2 --zb 2 > data/enum_$name.txt ) 2> logs/enum_$name.time
  echo "$name $(wc -l < data/enum_$name.txt)"
done <<L
cyl7x6_f3 cyl:7x6 0 3
cyl7x6_f4 cyl:7x6 0 4
cyl8x6_f3 cyl:8x6 0 3
cyl8x6_f4 cyl:8x6 0 4
flat7x6_f3_z0 flat:7x6 0 3
flat7x6_f4_z0 flat:7x6 0 4
flat7x6_f3_z2 flat:7x6 2 3
flat8x6_f3_z0 flat:8x6 0 3
flat8x6_f4_z0 flat:8x6 0 4
flat8x6_f3_z2 flat:8x6 2 3
L
