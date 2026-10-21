#!/bin/sh
# C1 reproduce (run from project root). Worker files are read, never written.
set -e
V=verify/dawson/C1-reproduce/rerun
PYTHONPATH=. .venv/bin/python $V/run_quotient32.py > $V/quotient32_stdout.txt   # = python -m dawson.quotient 32, outputs redirected (~380 s wall at load ~150)
cc -O2 -o $V/misere_c dawson/misere.c
$V/misere_c 70 $V/misere_c_70.bin > $V/misere_c_70.txt
cmp $V/misere_c_70.bin dawson/misere_c_70.bin                                       # identical to worker's table
PYTHONPATH=. .venv/bin/python -m dawson.check_quotient $V/quotient_Q32.pkl 70 $V/misere_c_70.bin
PYTHONPATH=. .venv/bin/python -m dawson.check_quotient dawson/quotient_Q32.pkl 70 $V/misere_c_70.bin
PYTHONPATH=. .venv/bin/python verify/dawson/C1-reproduce/indep_verify.py $V/quotient_Q32.pkl     # independent full verification
PYTHONPATH=. .venv/bin/python verify/dawson/C1-reproduce/indep_verify.py dawson/quotient_Q32.pkl
PYTHONPATH=. .venv/bin/python verify/dawson/C1-reproduce/kayles_check.py dawson/quotient_Q32.pkl 44
PYTHONPATH=. .venv/bin/python $V/check_quotient_mutation.py
PYTHONPATH=. .venv/bin/python verify/dawson/C1-reproduce/mutation_test2.py   # also runs mutation_test.py
