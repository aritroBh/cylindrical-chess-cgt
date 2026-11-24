#!/bin/zsh
# K60: toy validation runs through heavy.sh under /usr/bin/time -l.
cd "$(dirname $0)"
for seed in $@; do
  ../../heavy.sh /usr/bin/time -l ../../../../.venv/bin/python src/validate.py $seed 1500 1000 150 > logs/validate_$seed.out 2> logs/validate_$seed.err
done
