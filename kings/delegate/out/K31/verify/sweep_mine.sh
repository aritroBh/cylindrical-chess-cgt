#!/bin/bash
# own sweep: one pair a<r> on cyl:WxH, r=2..H-2.  usage: sweep_mine.sh Wmin Wmax Hmin Hmax out
for H in $(seq $3 $4); do for W in $(seq $1 $2); do for r in $(seq 2 $((H-2))); do
  nice -n 15 ./src/cls cyl $W $H a$r
done; done; done > $5
