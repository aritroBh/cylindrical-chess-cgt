#!/bin/bash
# own: single blocked pair on flat:WxH, every file, every rank (no mirror reduction)
for H in 5 6 7; do for W in 5 6 7 8 9 10; do for r in $(seq 2 $((H-2))); do for f in $(seq 0 $((W-1))); do
  fl=$(printf "\\x$(printf %x $((97+f)))")
  nice -n 15 ./src/cls flat $W $H $fl$r
done; done; done; done
