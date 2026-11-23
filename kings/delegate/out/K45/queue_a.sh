#!/bin/zsh
cd "$(dirname $0)"
for W in 10 11 12; do for f in 0,2,5 0,2,4 0,1,5 0,1,4 0,1,3 0,1,2; do ./run_a.sh $W $f; done; done
echo done > logs/queue_a.done
