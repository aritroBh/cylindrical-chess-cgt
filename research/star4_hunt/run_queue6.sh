#!/bin/bash
# ring annealing with ring4 (outcome score), seeds = 12-pawn ring *3 found by insertion
cd "$(dirname "$0")"
awk -F'\t' '1' seeds/ring_star3_12.txt > /dev/null
# C9 seeds only (width 9) and C8 seeds (width 8) are in the same file; split by max file letter
grep -E "[ ]i[0-9]" seeds/ring_star3_12.txt > seeds/ring_s3_c9.txt
grep -v -E "[ ]i[0-9]" seeds/ring_star3_12.txt > seeds/ring_s3_c8.txt
sa() { # name width seeds iters pmin pmax rng
  [ -f logs/$1.done ] && return
  nice -n 15 ./ring4 --cylinder --width $2 --single --max-entries 16777216 --evalbudget 3000000 --anneal $3 --iters $4 --temp 8 --pmin $5 --pmax $6 --rng $7 > out/$1.out 2> logs/$1.err && touch logs/$1.done
}
sa rsa_c9 9 seeds/ring_s3_c9.txt 6000 11 14 21
sa rsa_c8 8 seeds/ring_s3_c8.txt 8000 11 14 22
echo ALLDONE > logs/queue6.done
touch logs/queue3.done
