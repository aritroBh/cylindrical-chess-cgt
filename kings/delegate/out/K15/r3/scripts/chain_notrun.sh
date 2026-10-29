#!/bin/zsh
# K15 r3: after the survivor run (pid in logs/ctxexh_chunked_g.pid) finishes, root-only P-model check of the dud groups that were not confirmed before
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/r3
while kill -0 $(cat logs/ctxexh_chunked_g.pid) 2>/dev/null; do sleep 10; done
for b in cyl_7x6:cyl:7x6 cyl_8x6:cyl:8x6 cyl_8x8:cyl:8x8; do
  n=${b%%:*}; board=${b#*:}
  python3 scripts/chunkrun.py $board data/notrun_$n.in data/notrun_$n.out 2 --moves > logs/notrun_$n.log 2>&1
done
echo finished > logs/notrun.done
