#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
for j in "cyl:8x6 G8a_alone 1" "cyl:7x6 cyl7_alone 1" "cyl:8x6 G8a_blocked 1" "cyl:8x6 G8a_onemove 1" "cyl:8x6 G8a_alone 2" "cyl:8x6 G8a_gap 1"; do
  set -- ${=j}; ./scripts/run_chess.sh $1 $2 $3; echo "$j finished $(date +%T)" >> logs/chess_queue.log
done
echo finished >> logs/chess_queue.log
