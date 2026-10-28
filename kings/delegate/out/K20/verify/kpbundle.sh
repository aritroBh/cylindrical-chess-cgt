#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K20/verify
./kp --board flat:6x6 --cap 1 < flat6.pos > flat6.ch 2> flat6.ch.err
./kp --board cyl:6x6 --cap 1 < alone_cyl6.pos > alone_cyl6.ch 2> alone_cyl6.ch.err
echo done > kpbundle.done
