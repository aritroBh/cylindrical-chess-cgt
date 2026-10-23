#!/bin/bash
# annealing runs (mex score), one process
cd "$(dirname "$0")"
H=./h4
sa() { # name kind width seeds iters pmin pmax rng
  [ -f logs/$1.done ] && return
  nice -n 15 $H --$2 --width $3 --single --max-entries 16777216 --anneal $4 --iters $5 --temp 8 --pmin $6 --pmax $7 --score-mex --rng $8 > out/$1.out 2> logs/$1.err && touch logs/$1.done
}
cat seeds/w5p10_star3.txt seeds/cores3_all.txt > seeds/sa_seeds_all.txt
sa sa1_w5 flat 5 seeds/sa_seeds_all.txt 60000 9 12 11
sa sa1_w6 flat 6 seeds/sa_seeds_all.txt 60000 9 13 12
sa sa1_w7 flat 7 seeds/sa_seeds_all.txt 40000 9 13 13
echo ALLDONE > logs/slot2b.done
