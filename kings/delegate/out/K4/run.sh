#!/bin/sh
# K4 reproduce: every command, in order.  Run from anywhere; it changes to the project root.
# About 13 minutes in all on the Apple-silicon Mac it was developed on, nearly all of it in xrun.py
# (the second implementation); gafni.py for all ten boards takes about 30 s.  Peak RSS: gafni.py 84 MB
# on 5x5, xrun.py under 700 MB (sampled).
set -e
cd "$(dirname "$0")/../../../.."
export PYTHONPATH=.
PY="nice -n 10 .venv/bin/python"
K4=kings/delegate/out/K4

# kpsolve for check 1
nice -n 10 cc -O2 -o $K4/kp kings/kpsolve.c

# check 2 alone (pure CGT facts); gafni.py also runs it first and stops if it fails
$PY $K4/checks.py

# check 1 + signatures + candidates + difference tests; writes <flat|cyl>_<W>x<H>.jsonl, meta_*.json,
# candidates.json.  gafni.py exits with code 2 and writes FAILED_check1_*.json if kpsolve and the
# product solver differ anywhere.  Smallest boards first; 5x5 is run because 4x5 took 2.5 s (limit 10 min).
$PY $K4/gafni.py flat:3x4 cyl:3x4 flat:4x4 cyl:4x4 flat:3x5 cyl:3x5 flat:4x5 cyl:4x5
$PY $K4/gafni.py flat:5x5 cyl:5x5

# second implementation of the product solver (naive sweeps), compared with product.py on every
# K+P vs K position for the 16 test games and the negated matched candidates
$PY $K4/xrun.py flat:3x4 cyl:3x4 flat:4x4 cyl:4x4 > $K4/xrun_small.log
$PY $K4/xrun.py flat:3x5 cyl:3x5 flat:4x5 cyl:4x5 flat:5x5 cyl:5x5 > $K4/xrun_large.log

# integer scan x (+) n, n = -10..10
$PY $K4/tempo_scan.py flat:3x4 cyl:3x4 flat:4x4 cyl:4x4 flat:3x5 cyl:3x5 flat:4x5 cyl:4x5 flat:5x5 cyl:5x5 > $K4/tempo_scan.jsonl

# tables (printed to stdout)
$PY $K4/tables.py 3x4 4x4 3x5 4x5 5x5
$PY $K4/extras.py 3x4 4x4 3x5 4x5 5x5

# recompute every number the report quotes from the files above, assert the structural claims, print all tables
$PY $K4/claims.py
$PY $K4/mkreport.py

# not computed: the 3x3 board (kings/SPEC.md needs H >= 4).  The brief says 17 test games and 34-result signatures but lists 16
# games (see testgames.py); signatures here have 32 entries.
# verifier re-runs of the fix round (verify_A scripts in place, verify_B scripts as the copy vB_rerun/): sh $K4/fixlogs/run_verifiers.sh
