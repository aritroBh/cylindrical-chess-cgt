#!/bin/zsh
# usage: run_full.sh <board> <name>   (through heavy.sh): P model with real kings
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K20
$D/kp_p --board $1 --pmodel --cap 1 --threads 2 < $D/logs/$2.pos > $D/logs/$2.pmodel 2> $D/logs/$2.pmodel.err
