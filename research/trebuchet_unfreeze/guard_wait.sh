#!/bin/zsh
# wait until N main-unresolved cap-2 batches are done; kill (by PID) any cap-2 6x6 kpv above 3.9 GB
cd /Users/aritro/Downloads/Research/Chessendgames/research/trebuchet_unfreeze
N=$1
for i in $(seq 1 110); do
  [ $(ls logs/c2_u6_??.txt 2>/dev/null | wc -l) -ge $N ] && break
  ps -axo pid=,rss=,command= | grep "src/kpv --board cyl:6x6 --cap 2" | grep -v grep | grep -v "time -l" | while read pid rss rest; do
    if [ $rss -gt 3900000 ]; then echo "GUARD kill $pid rss=$rss" >> logs/stopped_pids.txt; kill $pid; fi; done
  sleep 5
done
ls logs/c2_u6_??.txt 2>/dev/null | wc -l
