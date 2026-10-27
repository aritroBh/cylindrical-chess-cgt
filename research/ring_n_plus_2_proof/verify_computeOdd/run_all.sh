#!/bin/sh
# Reproduce verify_computeOdd (run from the project root; at most 2 processes at a time, each under nice -n 15; no git, no pkill).
D=research/ring_n_plus_2_proof/verify_computeOdd
PY="env PYTHONPATH=. nice -n 15 .venv/bin/python -B -u"
$PY $D/diff_rules.py 1 600 > $D/logs/diff_rules_seed1.txt 2>&1                  # engine vs myeng.py, check3/eng.py, cylcgt/pawns.py (rules only)
$PY $D/run_a.py mine 9 25 R,Qo 6 > $D/logs/a_mine.txt 2>&1                      # (a) G+*h, h=0..6, my engine (keep / expire / raw flags)
$PY $D/run_a.py E 9 25 R,Qo 6 > $D/logs/a_E.txt 2>&1                            # (a) engine E = verify_compute/myeng.py
$PY $D/run_a.py C 9 25 R,Qo 6 > $D/logs/a_C.txt 2>&1                            # (a) engine C = check3/eng.py
$PY $D/run_a.py exh 9 11 R 4 > $D/logs/a_exh_R.txt 2>&1                         # (a) exhaustive, no early exit (about 200 s for R_11)
$PY $D/run_a.py exh 9 11 Qo 4 > $D/logs/a_exh_Qo.txt 2>&1
$PY $D/run_b.py 9 25 R,Qo 21 > $D/logs/b_reduced.txt 2>&1                       # (b) reduced graphs, three engines
for F in R Qo; do $PY $D/run_c.py $F 19 31 6 23 > $D/logs/c_$F.txt 2>&1; done   # (c) ins_6 isomorphism, Lemmas 2, 3 on the nodes
$PY $D/iso_small.py 11 17 > $D/logs/iso_small.txt 2>&1                          # information: n < 19
$PY $D/ext_a.py 27 41 > $D/logs/ext_a.txt 2>&1                                  # extension of (a)
