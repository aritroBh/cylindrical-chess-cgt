#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/verify
echo $$ > logs/queue1.pid
for a in "cyl:8x6 2 2" "flat:7x6 2 2" "flat:8x6 2 2" "cyl:8x6 3 2" "cyl:8x6 2 3" "cyl:7x6 3 2" "cyl:7x6 2 3" "flat:7x6 3 2" "flat:7x6 2 3"; do
  /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh scripts/runone.sh ${=a} > /dev/null 2>&1
done
echo finished > logs/queue1.done
