#!/bin/zsh
# K56 Part A, the three flat 8x6 groups again (the first run misread the board name "flat:8x6").
cd "$(dirname $0)"
seed=17
grep flat groups.txt | while read name board sh rest; do
  ./hrun.sh A_$name src/pr56f --board $board --root "$rest" --shuttle $sh --kmax 8 --sample 150 $seed
  seed=$((seed+1))
done
