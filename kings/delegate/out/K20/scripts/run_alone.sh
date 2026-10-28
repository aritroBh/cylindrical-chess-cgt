#!/bin/zsh
# D-model 'alone' predictions against real-king P model (and chess cap 1 on 6x6 boards); each through heavy.sh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K20
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
for b in flat:6x6 cyl:6x6 cyl:7x6 cyl:8x6; do
  n=${b//:/_}
  $H $D/kp_p --board $b --pmodel --cap 1 --threads 2 < $D/logs/alone_$n.pos > $D/logs/alone_$n.pmodel 2> $D/logs/alone_$n.pmodel.err
done
for b in flat:6x6 cyl:6x6; do
  n=${b//:/_}
  $H $D/kp --board $b --cap 1 --threads 2 < $D/logs/alone_$n.pos > $D/logs/alone_$n.chess 2> $D/logs/alone_$n.chess.err
done
