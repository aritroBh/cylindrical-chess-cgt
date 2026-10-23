#!/bin/bash
cd "$(dirname "$0")"
H4=/Users/aritro/Downloads/Research/Chessendgames/research/star4_hunt/h4
if [ "$1" = h4 ]; then : > h4_b5.out; for f in ch5/c_*; do nice -n 15 $H4 --flat --width 5 --evalbudget 1500000 --max-entries 4000000 --eval $f | grep -v '^#' >> h4_b5.out; done; echo done > h4_b5.done
else : > s2_b5.out; for f in ch5/c_*; do nice -n 15 timeout 300 ./s2n eval 5 $f | grep -v '^#' >> s2_b5.out; done; echo done > s2_b5.done; fi
