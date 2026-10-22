#!/bin/zsh
# Restart (00:20, 2026-10-22) of the cap-2 solve of the last open 1/8 side; the first run was killed after ~6 h.
cd "${0:A:h}/../.."
O=realchess/targets18
( time ./kings/kpsolve --board flat:8x8 --ep on --promote Q --cap 2 --threads 4 < $O/kp_eighth_cap2.txt > $O/kp_eighth_cap2.out.tmp ) 2> $O/kp_eighth_cap2.err \
  && mv $O/kp_eighth_cap2.out.tmp $O/kp_eighth_cap2.out
echo "exit $? at $(date)" >> $O/kp_eighth_cap2.err
