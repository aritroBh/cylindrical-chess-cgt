#!/bin/zsh
# K63 question 3: one optimal P line (ref3pv, = ref3m plus resolution order) for every disagreement position of the
# context tables, under a 2.2 GB RSS watchdog for my own child. usage: src/run_lines.sh <tag>...   -> logs/lines_<tag>.out
cd "$(dirname $0)/.."
for tag in "$@"; do
  zsh src/hrun.sh lines_$tag in/dis_$tag.pos zsh src/watch2.sh 2200000 bin/ref3pv --board pln:8x8 --moves --pv 160
done
echo done > logs/lines.done
