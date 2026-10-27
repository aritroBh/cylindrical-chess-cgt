#!/bin/zsh
# Python solver on the named counterexamples (E1 safe, E2, E2 safe, E4) and one control.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
cd $D; O=logs/compare_special.txt; : > $O
echo 'Kd4 kb5 Pb2 Pb3 pc3 pc4 b -' | nice -n 10 $PY scripts/local_py.py flat 4 5 0 3 safe >> $O
echo 'Ka1 kb5 Pb2 Pb3 pc3 pc4 b -' | nice -n 10 $PY scripts/local_py.py flat 4 5 0 3 >> $O
echo 'Ka5 kc6 Pc3 Pc4 pb4 pb5 b -' | nice -n 10 $PY scripts/local_py.py cyl 7 6 0 2 >> $O
echo 'Kc5 ka6 Pa3 Pa4 pb4 pb5 b -' | nice -n 10 $PY scripts/local_py.py cyl 7 6 0 2 >> $O
echo 'Ka5 kc6 Pc3 Pc4 pb4 pb5 b -' | nice -n 10 $PY scripts/local_py.py flat 5 6 0 4 safe >> $O
echo ALLDONE >> $O
