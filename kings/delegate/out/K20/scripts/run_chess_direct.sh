#!/bin/zsh
# chess (cap 1) 'alone' runs on the 6x6 boards, hard CPU limit 170 s each
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K20
for b in flat:6x6 cyl:6x6; do
  n=${b//:/_}
  ( ulimit -t 170; /usr/bin/time -l nice -n 15 $D/kp --board $b --cap 1 --threads 1 < $D/logs/alone_$n.pos > $D/logs/alone_$n.chess 2> $D/logs/alone_$n.chess.err; echo "exit $?" >> $D/logs/alone_$n.chess.err )
done
