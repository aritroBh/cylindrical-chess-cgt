#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/final
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
nice -n 15 ./bin/grp --nopass --W 5 --H 6 --F 3 --wmax 2 --bmax 2 --allow-passer --dumproots chk/g_np_5x6_pa1.tsv --out chk/g_np_5x6 > chk/g_np_5x6.json 2> chk/g_np_5x6.err
NOPASS=1 /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh ./watch.sh chk/py56.pid 2000000 1500 $PY ../f3/pycheck_np.py 5 6 3 2 2 chk/py_np_5x6_pa1.tsv 0 1 2> chk/py_np_5x6_pa1.err
echo "exit=$? $(date +%T)" > chk/py56.done
