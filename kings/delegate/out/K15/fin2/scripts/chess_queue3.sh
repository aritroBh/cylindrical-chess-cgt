#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
for j in "cyl:8x6 G8a_ctxWW 1" "cyl:8x6 G8a_ctxLL 1" "cyl:8x6 G8a_ctxWL 1"; do
  set -- ${=j}; ./scripts/run_chess.sh $1 $2 $3; echo "$j finished $(date +%T)" >> logs/chess_queue3.log
done
echo finished >> logs/chess_queue3.log
