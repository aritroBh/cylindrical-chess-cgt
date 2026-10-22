#!/bin/bash
# Reproduces every number in REPORT.md.  Run from the project root:
#   bash research/ring_min_independent/run_all.sh
# Needs: cc, .venv/bin/python (stdlib only).  ~10 minutes in total, <1 GB RSS, one process at a time.
set -e
D=research/ring_min_independent
cd "$(dirname "$0")/../.."
step() { echo "== $1  [$(date +%H:%M:%S)]"; }
step compile;           cc -O2 -Wall -Wno-unused-function -o $D/ring $D/ring.c
mkdir -p $D/data
step "C solver C3 (<=6 pawns)"; ( time nice -n 10 $D/ring -n 3 -p 6 --list $D/data/c3_star2.txt --all $D/data/c3_all.txt ) > $D/c3_run.out 2>&1
step "C solver C4 (<=7 pawns)"; ( time nice -n 10 $D/ring -n 4 -p 7 --list $D/data/c4_star2.txt --all $D/data/c4_all.txt ) > $D/c4_run.out 2>&1
step "claimed rings";   { nice -n 10 $D/ring -n 3 --pos "W: a2 a3 b2 / B: b7 c6 c7"; nice -n 10 $D/ring -n 4 --pos "W: a4 b2 c2 / B: b6 c5 d6 d7"; } > $D/claimed.out
step "variants (sensitivity)"
{ for v in "" "--textbook" "--noep" "--noep --textbook" "--race 1" "--race 2" "--lapse" "--lapse --textbook"; do
    for n in 3 4; do echo "### n=$n variant: [$v]"; eval "nice -n 10 $D/ring -n $n -p $((n+3)) $v" | grep -v '^pawns'; done; done; } > $D/variants.out
step "Python re-implementation C3"; ( time PYTHONPATH=. nice -n 10 .venv/bin/python $D/ring_check.py 3 6 $D/data/c3_all.txt ) > $D/c3_pycheck.out 2>&1
step "Python re-implementation C4"; ( time PYTHONPATH=. nice -n 10 .venv/bin/python $D/ring_check.py 4 7 $D/data/c4_all.txt ) > $D/c4_pycheck.out 2>&1
step "cylcgt comparison (done only after the counts)"
PYTHONPATH=. nice -n 10 .venv/bin/python $D/cmp_cylcgt.py > $D/cmp_cylcgt.out 2>&1
PYTHONPATH=. nice -n 10 .venv/bin/python $D/cmp_cylcgt_sample.py $D/data/c3_all.txt $D/data/c4_all.txt 4 > $D/cmp_cylcgt_sample.out 2>&1
step done
