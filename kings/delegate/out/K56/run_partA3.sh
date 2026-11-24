#!/bin/zsh
# K56 Part A, final run: Definition 4.8, pass-robust and the budget (tempo-exact) test for the nine groups.
# T3_c87 needs 2.8 GB (14.3 million nodes) and is run last, alone.
cd "$(dirname $0)"
grep -v T3_c87 groups.txt | while read name board sh rest; do
  ./hrun.sh B_$name src/pr56b --board $board --root "$rest" --shuttle $sh --kmax 8
done
