#!/bin/bash
cd /Users/aritro/Downloads/Research/Chessendgames/research/star4_rings/core_wall
for p in 8 9 10; do for cfg in "4 0" "5 0" "5 1"; do set -- $cfg; nice -n 15 ./samp 6 $p $1 $2 40000 99 2>&1 >/dev/null | tail -1; done; done
