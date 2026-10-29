#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
until grep -q "^finished" logs/chess_queue.log 2>/dev/null; do sleep 30; done
./scripts/run_chess2.sh cyl:8x6 G8_states 1 --moves; echo "G8_states cap1 moves done $(date +%T)" >> logs/chess_queue2.log
./scripts/run_chess2.sh cyl:8x6 G8_states 2 --moves; echo "G8_states cap2 moves done $(date +%T)" >> logs/chess_queue2.log
echo finished >> logs/chess_queue2.log
