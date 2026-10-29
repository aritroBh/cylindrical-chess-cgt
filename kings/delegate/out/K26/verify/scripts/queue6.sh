#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/verify
echo $$ > logs/queue6.pid
for b in cyl:7x6 flat:7x6; do
  tg=${b/:/}
  for ((i=0;i<40;i++)); do
    nice -n 15 python3 scripts/ref_under.py $b 2 2 3 $i/40 2>/dev/null >> logs/under_${tg}_22.txt
  done
done
echo finished > logs/queue6.done
