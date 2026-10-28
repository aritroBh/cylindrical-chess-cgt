#!/bin/zsh
# sequential cap-1 chess runs of the 16 four-pawn king-move children, one position per kp process, each under heavy.sh,
# 3 GB RSS watchdog and 20 min wall limit.
K=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K27
i=0
while read -r line; do
  i=$((i+1))
  echo "$line" > $K/work/c16_$i.in
  /usr/bin/time -l $K/../../heavy.sh $K/scripts/watch2.sh $K/logs/run2/pid_kp.txt 3000000 1200 $K/work/kp --board flat:7x6 --cap 1 --threads 2 < $K/work/c16_$i.in > $K/logs/run2/c16_$i.out 2> $K/logs/run2/c16_$i.err
  echo "$i done $(date)" >> $K/logs/run2/progress.txt
done < $K/logs/inputs/ch16.txt
echo ALLDONE >> $K/logs/run2/progress.txt
