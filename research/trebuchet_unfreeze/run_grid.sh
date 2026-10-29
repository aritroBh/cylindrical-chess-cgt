#!/bin/zsh
# usage: run_grid.sh K   (runs jobs K, K+2, K+4, ... of jobs.txt; each line: label|board|args)
cd /Users/aritro/Downloads/Research/Chessendgames/research/trebuchet_unfreeze
echo $$ > logs/runner$1.pid
n=0
while IFS='|' read -r label board args; do
  n=$((n+1)); [ $(( (n-1) % 2 )) -eq $1 ] || continue
  [ -s logs/g_$label.txt ] && continue
  nice -n 15 /usr/bin/time -l src/kpv --board $board ${=args} --moves < data/p4_all12.txt > logs/g_$label.txt 2> logs/g_$label.err
done < jobs.txt
