#!/bin/zsh
# referee-2 random sample: n=5..8, 3 density bands each, 100000 stoppers per run (nice 15, each run well under 1 CPU minute)
cd "$(dirname $0)/.."
: > logs/rand_mine.txt
for nn in 5 6 7 8; do
  for band in "0.05 0.15" "0.15 0.35" "0.30 0.60"; do
    p1=${band% *}; p2=${band#* }; m=$((nn+4)); seed=$((nn*100+7))
    echo "# n=$nn p=[$p1,$p2] seed=$seed K=4 M=$m count=100000" >> logs/rand_mine.txt
    nice -n 15 ./chk rand $nn 100000 $seed $p1 $p2 4 $m >> logs/rand_mine.txt
  done
done
