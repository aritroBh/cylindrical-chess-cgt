#!/bin/zsh
# usage: run_check.sh <board> <logname>   (run through heavy.sh)
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K20
b=$1; n=${b//:/_}
cfgs=("${(@f)$(grep '^CONFIG' $D/logs/${n}_free.log | sed -E 's/^CONFIG (.*) : nodes.*/\1/' | sed 's/ *$//')}")
/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python $D/scripts/check_kg.py $b $D/logs/roots_$n.txt "${cfgs[@]}"
