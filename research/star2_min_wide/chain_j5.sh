#!/bin/bash
# 7-pawn connected roots: contiguous blocks of 800 rows at 15%, 50%, 85% of each (width, split); cylcgt in whole-board mode (like-for-like with the scanner)
# and in the default (sum) model.
cd "$(dirname "$0")"
while read W NW TOT; do
  for PCT in 15 50 85; do LO=$(( TOT * PCT / 100 )); HI=$(( LO + 800 ))
    WHOLE=1 ./run_conn.sh $W 7 $NW $LO $HI
  done
done <<LIST
5 2 97327
5 3 423295
6 2 21725
6 3 265880
7 3 54345
LIST
while read W NW TOT; do
  for PCT in 15 50 85; do LO=$(( TOT * PCT / 100 )); HI=$(( LO + 800 ))
    ./run_conn.sh $W 7 $NW $LO $HI
  done
done <<LIST
5 2 97327
5 3 423295
6 2 21725
6 3 265880
7 3 54345
LIST
