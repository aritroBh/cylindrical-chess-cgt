#!/bin/bash
# beyond K31's boundary: H=13..15 (W 4..14), and W=27..34 for H=4..6.   usage: sweep_ext_mine.sh out
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/verify
for H in 13 14 15; do for W in 4 5 6 7 8 9 10 11 12 13 14; do for r in $(seq 2 $((H-2))); do nice -n 15 ./src/cls cyl $W $H a$r; done; done; done > $1
for H in 4 5 6; do for W in 27 28 29 30 31 32 33 34; do for r in $(seq 2 $((H-2))); do nice -n 15 ./src/cls cyl $W $H a$r; done; done; done >> $1
