#!/bin/zsh
# K60 referee: toy brute force through heavy.sh under /usr/bin/time -l.
cd "$(dirname $0)"
for seed in $@; do
  ../../../heavy.sh /usr/bin/time -l ../../../../../.venv/bin/python src/r60run.py $seed 3000 250 > logs/toys_$seed.out 2> logs/toys_$seed.err
done
