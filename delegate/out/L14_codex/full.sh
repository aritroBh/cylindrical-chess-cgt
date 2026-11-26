#!/bin/sh
set -eu
export PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1
d=delegate/out/L14_codex
for width in 1 2 3; do
    nice -n 15 .venv/bin/python "$d/census.py" "$width" 6 all
done
nice -n 15 .venv/bin/python "$d/census.py" 4 5 all
# ponytail: partition the largest group by its first occupied rank to bound memo size.
for rank in 0 1 2 3 4 5; do
    nice -n 15 .venv/bin/python "$d/census.py" 4 6 all "$rank" 6
done
