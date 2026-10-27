#!/bin/sh
set -eu
for rank in 2 3 4 5; do
  for phase in 0 1; do
    log="research/odd_n_plus_2/logs/c9_w4_d2_r${rank}_p${phase}.log"
    PYTHONPATH=. .venv/bin/python -u research/odd_n_plus_2/search.py 9 4 2 "$rank" "$phase" --batch 40 --bits 22 >"$log" 2>&1
  done
done
