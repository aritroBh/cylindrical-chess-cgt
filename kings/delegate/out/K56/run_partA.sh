#!/bin/zsh
# K56 Part A: Definition 4.8 and pass-robust tests for the nine groups, with 150 sampled P values each (for validation).
cd "$(dirname $0)"
seed=11
while read name board sh rest; do
  ./hrun.sh A_$name src/pr56 --board $board --root "$rest" --shuttle $sh --kmax 8 --sample 150 $seed
  seed=$((seed+1))
done < groups.txt
