#!/bin/zsh
# extended-battery and additivity check, one heavy run per board (each well under 20 min)
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K20
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
for b in flat:6x6 cyl:6x6 cyl:8x6 flat:8x6 cyl:7x6; do
  n=${b//:/_}
  $H $D/kg --board $b --maxpairs 2 --ext --pairs --maxex 2 > $D/logs/ext_$n.log 2> $D/logs/ext_$n.err
done
