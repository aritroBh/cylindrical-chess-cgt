#!/bin/zsh
cd "$(dirname $0)"
for W in 9 8 7 6; do ./queue_ball.sh $W; done
echo done > logs/queue_ball_small.done
