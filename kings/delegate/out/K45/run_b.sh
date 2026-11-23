#!/bin/zsh
# K45 implementation B (own solver, battery configurations only).  Usage: run_b.sh W
cd "$(dirname $0)"
W=$1
[[ -f logs/B_$W.done ]] && exit 0
../../heavy.sh ./bin/b45 --W $W --reach logs/B_${W}_reach.txt < configs_all.txt > logs/B_$W.out 2> logs/B_$W.err
echo "rc=$?" > logs/B_$W.done
