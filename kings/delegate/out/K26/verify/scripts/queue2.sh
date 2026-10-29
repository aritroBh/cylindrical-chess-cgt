#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/verify
echo $$ > logs/queue2.pid
for spec in "ZB cyl:7x6 ef 3 4" "ZB cyl:8x6 efg 3 24" "ZC cyl:8x6 efg 3 24" "ZB flat:7x6 efg 3 24"; do
  set -- ${=spec}
  for ((i=0;i<$5;i++)); do
    nice -n 15 python3 scripts/dud_ctx.py $1 $2 $3 $4 $i/$5 >> logs/ctx_exh_$1_${2/:/}.txt 2>&1
  done
done
echo finished > logs/queue2.done
