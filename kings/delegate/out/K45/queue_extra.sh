#!/bin/zsh
cd "$(dirname $0)"
./run_ball.sh 10 0,2,6
./run_ball.sh 10 0,3,6
echo done > logs/queue_extra.done
