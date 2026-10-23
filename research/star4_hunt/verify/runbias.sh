#!/bin/bash
cd "$(dirname "$0")"
H4=/Users/aritro/Downloads/Research/Chessendgames/research/star4_hunt/h4
: > h4_bias.out; : > s2_bias.out
if [ "$1" = h4 ]; then
 for w in 4 5 6; do for f in ch4/b${w}_*; do nice -n 15 $H4 --flat --width $w --eval $f | grep -v '^#' >> h4_bias.out; done; done; echo done > h4_bias.done
else
 for w in 4 5 6; do for f in ch4/b${w}_*; do nice -n 15 ./s2n eval $w $f | grep -v '^#' >> s2_bias.out; done; done; echo done > s2_bias.done
fi
