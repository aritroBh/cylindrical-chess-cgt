#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/verify
echo $$ > logs/queue_u32.pid
for ((i=0;i<24;i++)); do
  nice -n 15 python3 scripts/ref_under.py cyl:8x6 3 2 3 $i/24 2>/dev/null >> logs/under_cyl8x6_32.txt
done
echo finished > logs/queue_u32.done
