#!/bin/sh
# Evaluate each finite reduced-game base with cylcgt canonical-form arithmetic.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
SRC=$ROOT/research/ring_n_plus_2_proof
OUT=$ROOT/research/ring_q_family_check
cd "$ROOT"
mkdir -p "$OUT/logs"

for n in 8 10 12 14 16 18 20 22; do
    PYTHONPATH=.:"$SRC" nice -n 15 .venv/bin/python "$OUT/run_source_check.py" reduced_value.py Q "$n" \
        > "$OUT/logs/reduced_value_Q_$n.txt" 2> "$OUT/logs/reduced_value_Q_$n.stderr.txt"
done
