#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/verify/r2
HV=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
for spec in "7 7 3 26" "8 8 3 26" "9 9 3 26" "10 10 3 26" "11 11 3 26" "12 12 3 14" "12 12 15 26"; do
  set -- ${=spec}
  $HV ./sweep.sh $1 $2 $3 $4 out/s_h$1_$3.txt
done
echo ALLDONE > out/sweeps_done.txt
