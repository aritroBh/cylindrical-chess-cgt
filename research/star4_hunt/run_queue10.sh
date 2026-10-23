#!/bin/bash
# flat w2 and w3, every pawn count (single component), splits nw<=nb
cd "$(dirname "$0")"
source ./scanlib.sh
while [ ! -f logs/queue8.done ]; do sleep 20; done
for p in 8 9 10 11 12 13 14; do
  for ((nw=2; nw<=p/2; nw++)); do nb=$((p-nw)); [ $nb -gt 15 ] && continue
    if [ $nw -eq $nb ]; then scan w3all flat 3 $nw $nb 1 --colsym; else scan w3all flat 3 $nw $nb 1; fi
  done
done
echo ALLDONE > logs/queue10.done
