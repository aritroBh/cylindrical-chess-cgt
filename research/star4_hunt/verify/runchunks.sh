#!/bin/bash
# usage: runchunks.sh PROG(h4|s2) WIDTH PREFIX OUT ; evaluates chunk files ch2/PREFIX* one process at a time (bounded memory)
cd "$(dirname "$0")"
H4=/Users/aritro/Downloads/Research/Chessendgames/research/star4_hunt/h4
prog=$1; w=$2; pre=$3; out=$4; : > $out
for f in ch2/${pre}*; do
  if [ $prog = h4 ]; then nice -n 15 $H4 --flat --width $w --eval $f | grep -v '^#' >> $out
  else nice -n 15 ./s2 eval $w $f | grep -v '^#' >> $out; fi
done
