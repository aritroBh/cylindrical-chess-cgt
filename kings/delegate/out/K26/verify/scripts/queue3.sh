#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/verify
echo $$ > logs/queue3.pid
for ((i=0;i<40;i++)); do
  nice -n 15 python3 scripts/ref_under.py cyl:8x6 2 2 3 $i/40 2>/dev/null >> logs/under_cyl8x6_22.txt
done
echo finished > logs/queue3.done
