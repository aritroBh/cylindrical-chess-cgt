#!/bin/zsh
cd "$(dirname $0)"
./run_ball.sh 14 0,1,4 &
./run_ball.sh 16 0,1,4
wait
echo done > logs/queue_wide.done
