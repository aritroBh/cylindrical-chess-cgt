#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K38/verify
for b in cyl:7x6 flat:7x6; do
  echo "== kpsolve cap2 $b"
  /usr/bin/time -l /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh ./bin/kpsolve --board $b --cap 2 --moves < pos.txt
done > logs/kpsolve_cap2.log 2>&1
