#!/bin/zsh
# P-model full-board runs with a hard CPU limit of 150 s each (below the one-CPU-minute-ish rule by design; killed by SIGXCPU otherwise)
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K20
for n in full_flat8x6 full_far_flat8x6; do
  ( ulimit -t 150; /usr/bin/time -p nice -n 15 $D/kp_p --board flat:8x6 --pmodel --cap 1 --threads 1 < $D/logs/$n.pos > $D/logs/$n.pmodel 2> $D/logs/$n.pmodel.err; echo "exit $?" >> $D/logs/$n.pmodel.err )
done
