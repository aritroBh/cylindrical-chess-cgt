#!/bin/zsh
# K57: Lemma 2 (criterion B1) on the K56 referee's toy groups, three seeds.
cd "$(dirname $0)"
for s in 11 12 13; do ./hrun.sh toy_$s python3 src/toy57.py $s 1500 60; done
