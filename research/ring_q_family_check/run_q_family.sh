#!/bin/sh
# Reproduce the Q-family pump, reduced-graph, and unreduced checks from the
# current ring_n_plus_2_proof runner, writing all outputs only in this folder.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
SRC=$ROOT/research/ring_n_plus_2_proof
OUT=$ROOT/research/ring_q_family_check
cd "$ROOT"
mkdir -p "$OUT/logs"
cc -O2 -DMAXN=64 -o "$OUT/rg" research/ring_family_proof/rg.c -lpthread

nice -n 15 python3 "$OUT/run_source_check.py" pump_verify.py Q 8 60 > "$OUT/logs/pump_Q_8_60.txt" 2> "$OUT/logs/pump_Q_8_60.stderr.txt"
FIXC=9 nice -n 15 python3 "$OUT/run_source_check.py" pump_verify.py Q 22 60 > "$OUT/logs/pump_Q_fixc9.txt" 2> "$OUT/logs/pump_Q_fixc9.stderr.txt"
PYTHONPATH=.:"$SRC" nice -n 15 .venv/bin/python "$OUT/run_source_check.py" reduced_cyl.py Q 8 10 12 14 16 18 20 22 24 > "$OUT/logs/reduced_cyl_Q.txt" 2> "$OUT/logs/reduced_cyl_Q.stderr.txt"

nice -n 15 python3 "$OUT/run_rg_sweep.py" 8 60 > "$OUT/logs/unreduced_Q_8_60.txt" 2> "$OUT/logs/unreduced_Q_8_60.stderr.txt"
