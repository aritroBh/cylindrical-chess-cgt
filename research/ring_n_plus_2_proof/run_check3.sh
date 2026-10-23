#!/bin/sh
# Third, independent program for the family P: the T50 verifier's engine check3/eng.py (written from the rules, not from rg.c;
# copies with the family P added) and the cylcgt canonical value of the reduced game. One process at a time, about 3 minutes.
# Run from the project root after run_all.sh (needs rg).
set -e
D=research/ring_n_plus_2_proof; C=$D/check3; L=$D/logs
export PYTHONDONTWRITEBYTECODE=1
(cd $C && nice -n 15 python3 -B unreduced.py 8 10 12 14 16 18 20 22) > $L/c3_unreduced_P.txt
(cd $C && nice -n 15 python3 -B red.py P 8 10 12 14 16 18 20 22 24) > $L/c3_reduced_P.txt
(cd $C && nice -n 15 python3 -B pump.py pump P 12 18 20 22 24 26) > $L/c3_pump_P.txt
(cd $C && nice -n 15 python3 -B pump.py nodes P 18 20) > $L/c3_lemma3_nodes_P.txt
(cd $C && nice -n 15 python3 -B lem.py l2 P 8000 1; nice -n 15 python3 -B lem.py l3 P 8000 1; nice -n 15 python3 -B lem.py l3 P 3000 2 3) > $L/c3_lemma23_random_P.txt
(cd $C && nice -n 15 python3 -B split_count.py 18) > $L/c3_split_P.txt
PYTHONPATH=.:$D nice -n 15 .venv/bin/python $D/reduced_value.py P 8 10 12 14 16 18 20 > $L/reduced_value_P.txt
