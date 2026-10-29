#!/bin/zsh
# K15 r3: ref3 over the sampled chunks, 25 positions each (about 40 CPU-s), unlocked as allowed for runs under one CPU-minute: nice 15, ulimit -t 58, one process at a time.
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/r3
for t in c8x6:cyl:8x6 c7x6:cyl:7x6 strictA8:cyl:8x6; do
  tag=${t%%:*}; board=${t#*:}
  for f in xs/$tag.chunk*.in; do
    o=${f%.in}.out
    [[ -s $o ]] && continue
    ( ulimit -t 58; nice -n 15 bin/ref3 --board $board < $f > $o 2> ${o%.out}.err )
    echo "done $f exit=$? lines=$(wc -l < $o) $(date +%T)" >> logs/ref3_chunks.log
  done
done
echo finished >> logs/ref3_chunks.log
