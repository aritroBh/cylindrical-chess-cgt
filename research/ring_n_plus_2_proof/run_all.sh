#!/bin/sh
# Evidence for the even n+2 family P_n = W5 B7 W4 W4B7 B6 W3B6 (W2 B4)^((n-6)/2), n even >= 8 (whole-board game).
# Uses T50's engine research/ring_family_proof/rg.c (unchanged) and copies of T50's fam.py/graph.py/pump_verify.py/
# reduced_cyl.py with the family P added. Run from the project root.
set -e
D=research/ring_n_plus_2_proof
cc -O2 -DMAXN=64 -o $D/rg research/ring_family_proof/rg.c -lpthread
nice -n 15 python3 $D/pump_verify.py P 8 60 > $D/logs/pump_P_8_60.txt
FIXC=12 nice -n 15 python3 $D/pump_verify.py P 18 60 > $D/logs/pump_P_fixc12.txt
PYTHONPATH=.:$D nice -n 15 .venv/bin/python $D/reduced_cyl.py P 8 10 12 14 16 18 20 22 > $D/logs/reduced_cyl_P.txt
for n in $(seq 8 2 60); do python3 -c "print(' '.join(['W5','B7','W4','W4B7','B6','W3B6']+['W2','B4']*(($n-6)//2)))"; done | $D/rg solve 3 > $D/logs/unreduced_P_8_60.txt
# The *3 family Q_n = W4 B7 (B4 W2)^((n-8)/2) W3B6 W3 W2B5 B5 W2 B4, n even >= 8 (n+2 pawns); Q_8 is the C8 *3 hit.
nice -n 15 python3 $D/pump_verify.py Q 8 60 > $D/logs/pump_Q_8_60.txt
FIXC=9 nice -n 15 python3 $D/pump_verify.py Q 22 60 > $D/logs/pump_Q_fixc9.txt
PYTHONPATH=.:$D nice -n 15 .venv/bin/python $D/reduced_cyl.py Q 8 10 12 14 16 18 20 22 24 > $D/logs/reduced_cyl_Q.txt
for n in $(seq 8 2 60); do python3 -c "print(' '.join(['W4','B7']+['B4','W2']*(($n-8)//2)+['W3B6','W3','W2B5','B5','W2','B4']))"; done | $D/rg solve 3 > $D/logs/unreduced_Q_8_60.txt
