#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16/verify
for t in "g_f76 flat:7x6" "g_c86 cyl:8x6" "g_c66 cyl:6x6" "g_c76 cyl:7x6" "g_f66_3 flat:6x6"; do
  set -- ${=t}
  /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh ./kpp --board $2 --pmodel < $1.in > $1.out 2> $1.err
done
