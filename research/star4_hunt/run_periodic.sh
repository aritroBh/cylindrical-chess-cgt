#!/bin/bash
cd "$(dirname "$0")"
for w in 4 5 6 7 8; do
  nice -n 15 ./h4 --flat --width $w --max-entries 16777216 --evalbudget 3000000 --eval seeds/periodic2_w$w.txt > out/periodic2_w$w.tsv 2> logs/periodic2_w$w.err
done
echo DONE > logs/periodic.done
