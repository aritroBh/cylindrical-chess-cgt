#!/bin/zsh
# K15 r3: run ref3 (independent P solver) over the sampled chunks, one heavy.sh call per chunk (slot released between chunks).
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/r3
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
for t in c8x6:cyl:8x6 c7x6:cyl:7x6 strictA8:cyl:8x6; do
  tag=${t%%:*}; board=${t#*:}
  for f in xs/$tag.chunk*.in; do
    o=${f%.in}.out
    [[ -s $o ]] && continue
    ( ulimit -v 3000000; $H bin/ref3 --board $board < $f > $o 2> ${o%.out}.err )
    echo "done $f $(date +%T)" >> logs/ref3_chunks.log
  done
done
echo finished >> logs/ref3_chunks.log
