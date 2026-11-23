#!/bin/zsh
cd "$(dirname $0)"
W=$1
for f in 0,1,4 0,2,5 0,2,4 0,1,5 0,1,3 0,1,2; do ./run_ball.sh $W $f; done
echo done > logs/queue_ball_$W.done
