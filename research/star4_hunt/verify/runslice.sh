#!/bin/bash
cd "$(dirname "$0")"
H4=/Users/aritro/Downloads/Research/Chessendgames/research/star4_hunt/h4
: > h4_slice.out
for f in ch3/s_*; do nice -n 15 $H4 --flat --width 5 --eval $f | grep -v '^#' >> h4_slice.out; done
echo done > h4_slice.done
