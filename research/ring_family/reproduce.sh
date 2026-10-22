#!/bin/zsh
# T41 ring_family: rebuild and re-run the main checks.  Run from anywhere; uses .venv/bin/python.
set -e
ROOT=/Users/aritro/Downloads/Research/Chessendgames
cd $ROOT/research/ring_family
# 1. solvers (C): ringeval = scanner core with a width-10 layout; ringeval_w = 128-bit masks, widths up to 21
cc -O2 -DSTRIDE=8  -o ringeval8 ringeval.c
cc -O2 -DSTRIDE=10 -o ringeval  ringeval.c
python3 mkwide.py && cc -O2 -DSTRIDE=21 -o ringeval_w ringeval_w.c
cc -O2 -DSTRIDE=10 -o coresearch coresearch.c
cd $ROOT
export PYTHONPATH=$ROOT
# 2. the two families, n = 5..21, written to research/ring_family/families.tsv
.venv/bin/python research/ring_family/family.py 21
# 3. cylcgt (independent Python solver) on family members (seconds to minutes each)
.venv/bin/python research/ring_family/cyl_run.py "$(.venv/bin/python -c "import sys;sys.path.insert(0,'research/ring_family');from family import *;print(cstr(odd(9)))")"
.venv/bin/python research/ring_family/cyl_run.py "$(.venv/bin/python -c "import sys;sys.path.insert(0,'research/ring_family');from family import *;print(cstr(even(8)))")"
# 4. reduced game graph: pumping isomorphism (C solver) and independent re-implementation (cylcgt move generator)
.venv/bin/python research/ring_family/pump_check.py odd 2 9
.venv/bin/python research/ring_family/pump_check.py even 1 7
.venv/bin/python research/ring_family/pump_check_py.py odd 3 6
.venv/bin/python research/ring_family/pump_check_py.py even 2 5
.venv/bin/python research/ring_family/graph_solve.py research/ring_family/dumps/odd_k3.tsv research/ring_family/dumps/even_k2.tsv
