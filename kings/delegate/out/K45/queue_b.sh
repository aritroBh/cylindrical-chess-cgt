#!/bin/zsh
cd "$(dirname $0)"
for W in 11 12; do ./run_b.sh $W; done
echo done > logs/queue_b.done
