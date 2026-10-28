#!/bin/zsh
# referee's independent chess solver (verify/ownchess.cpp) on the 16 four-pawn king-move children, bound A for the Black wins,
# bound B for the White wins, both for line 12; one process per run under heavy.sh, 3 GB RSS watchdog, 20 min wall limit.
K=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27
for spec in "1 0" "2 0" "3 0" "4 0" "5 0" "6 0" "7 1" "8 1" "9 1" "10 0" "11 0" "12 0" "12 1" "13 0" "14 1" "15 1" "16 1"; do
  set -- ${=spec}
  sed -n "${1}p" $K/logs/inputs/ch16.txt > $K/work/o_$1_$2.in
  $K/../../heavy.sh $K/scripts/watch2.sh $K/logs/run2/pid_own.txt 3000000 1200 $K/work/ownchess 7 6 $2 < $K/work/o_$1_$2.in > $K/logs/run2/own_$1_$2.out 2> $K/logs/run2/own_$1_$2.err
  echo "$1 $2 done $(date)" >> $K/logs/run2/progress_own.txt
done
echo ALLDONE >> $K/logs/run2/progress_own.txt
