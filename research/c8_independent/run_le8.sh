#!/bin/zsh
# Second program for the paper's "rings on C5..C8 with at most eight pawns: *2 only in the 14 eight-pawn rings on C5".
# C5 p8 done (out_f5_p8.txt: 14 *2). C5 p5-7 and C6 p6-8 have T45's ring solver as second program; C7 p7-8 and C8 p8 run here.
cd "${0:A:h}"
for fp in "7 7" "7 8" "8 8"; do
  set -- ${=fp}; start=$(date +%s)
  nice -n 15 ./c8check_gen --enum 0 1 $1 $2 > out_f$1_p$2.txt 2> out_f$1_p$2.err
  echo "[$(date +%H:%M)] f=$1 p=$2 done in $(( $(date +%s) - start )) s: $(grep -v STAR out_f$1_p$2.txt | head -1)" >> progress_le8.txt
done
echo "[$(date +%H:%M)] ALL DONE" >> progress_le8.txt
