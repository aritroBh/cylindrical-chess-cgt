#!/bin/sh
# Evidence for PROOF_odd.md: R_n = *2 and Qo_n = *3 for odd n >= 11 (whole-board game).  Run from the project root, one job at a time.
# A = T50's rg.c (built by ../run_all.sh as research/ring_n_plus_2_proof/rg), E = verify_compute/myeng.py.  Logs are written next to this file
# (check_odd_*.log, base_cases.log) and into ../logs (pump_*_fixc.txt).  The rg full searches and the cylcgt rebuilds for odd n are in
# ../logs/unreduced_R_9_59.txt, unreduced_Qo_9_59.txt, reduced_cyl_R.txt, reduced_cyl_Qo.txt (written by ../run_all.sh).
set -e
D=research/ring_n_plus_2_proof
[ -x $D/rg ] || cc -O2 -DMAXN=64 -o $D/rg research/ring_family_proof/rg.c -lpthread
for F in R Qo; do FIXC=6 nice -n 15 python3 $D/pump_verify.py $F 19 59 > $D/logs/pump_${F}_fixc.txt; done      # cut c = 6, base n0 = 19
for F in R Qo; do PYTHONPATH=. nice -n 15 .venv/bin/python -u $D/odd/check_odd.py $F > $D/odd/check_odd_$F.log; done   # about 1 and 3 min
PYTHONPATH=. nice -n 15 .venv/bin/python -u $D/odd/base_cases.py 21 > $D/odd/base_cases.log                        # about 1 min
