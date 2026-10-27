#!/bin/bash
cd /Users/aritro/Downloads/Research/Chessendgames/research/star4_rings/core_wall
for p in 6 7; do for cfg in "4 0" "5 0" "5 1"; do nice -n 15 ./gen 6 $p $cfg count; done; done
