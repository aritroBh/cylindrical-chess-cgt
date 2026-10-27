#!/bin/zsh
# Reproduce every K19 number. Run from anywhere. Light runs (seconds); the kp/kp_p runs take seconds each as well.
R=/Users/aritro/Downloads/Research/Chessendgames
D=$R/kings/delegate/out/K19
export PYTHONPATH=$R
PY=$R/.venv/bin/python
cc -O2 -o $D/kp $R/kings/kpsolve.c -lpthread
cc -O2 -o $D/kp_p $R/kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread
cd $D/scripts
$PY claim51.py  > ../logs/claim51.log     # 5.1 (L1), (L3), White sorties
$PY claim51b.py > ../logs/claim51b.log    # 5.1 Black sorties (mirror), Black's legal moves
$PY claim52.py  > ../logs/claim52.log     # 5.2 local games
$PY claim55.py  > ../logs/claim55.log     # 5.5
$PY claim56.py  > ../logs/claim56.log     # 5.6 mu and T
for s in s51 s52 s52f s52a s52h s55; do $PY fullboard.py own $s > ../logs/own_P_$s.log; done   # own P solver
./run_kpp.sh                                                       # kp_p (P) on all lists
$PY fullboard.py list s52h > ../logs/in_s52h.txt; $D/kp_p --board cyl:7x6 --ep on --promote QRBN --cap 1 --pmodel < ../logs/in_s52h.txt > ../logs/kpp_s52h.txt
$R/kings/delegate/heavy.sh ./run_kp_chess.sh                       # kp (chess), through the shared lock
$PY compare.py
$PY xcheck_movegen.py   # (heavy: kp --moves on ~1000 positions; use heavy.sh)
$PY xcheck_p.py; $PY xcheck_local.py
$PY make_edits.py
