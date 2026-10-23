#!/bin/sh
# Independent recomputation for P_n (lens: INDEPENDENT COMPUTATION).  Does not use rg.c or cylcgt's game-value code.
# Engines: t50/ = unchanged copies of the T50 verifier engine (eng.py, red.py, pump.py); myeng.py = my own engine.
# Run from the project root:  sh research/ring_n_plus_2_proof/verify_compute/run_all.sh     (about 15 minutes, one process at a time)
# diff_rules.py also imports cylcgt/pawns.py and uses ONLY its rule predicates (moves, passed, promote_distance) as a reference.
set -e
D=research/ring_n_plus_2_proof/verify_compute
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.
PY="nice -n 15 .venv/bin/python -B"
mkdir -p $D/logs
for s in 1 2 3; do $PY $D/diff_rules.py $s 1500; done > $D/logs/diff_rules.txt
$PY $D/run_a.py 8 30  > $D/logs/a_outcomes_8_30.txt
$PY $D/run_a.py 32 60 > $D/logs/a_outcomes_32_60.txt
$PY $D/run_bc.py 8 60 > $D/logs/bc_stdout_8_60.txt      # also writes logs/b_reduced_8_60.txt and logs/c_insertion_8_60.txt
$PY $D/run_lemma2.py 18 22 26 > $D/logs/lemma2_nodes.txt
$PY $D/extra_checks.py 18 > $D/logs/extra_checks.txt
$PY $D/run_race_rules.py > $D/logs/race_rules.txt
$PY $D/run_calibration.py > $D/logs/calibration.txt
$PY $D/compare_logs.py > $D/logs/compare_logs.txt
cat $D/logs/compare_logs.txt
