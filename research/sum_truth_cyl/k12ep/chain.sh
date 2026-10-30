#!/bin/bash
echo $$ > chain.pid
cd /Users/aritro/Downloads/Research/Chessendgames/research/sum_truth_cyl/k12ep
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
for a in "6 6 3" "8 6 2" "7 6 3"; do
  set -- $a
  nice -n 15 ../../../.venv/bin/python run_ep.py $1 $2 $3 > ep_$1x$2.log 2>&1
done
