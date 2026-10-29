#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/f3
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
NOPASS=1 $H perl -e 'alarm 1100; exec @ARGV' /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python pycheck_np.py 5 6 3 2 2 chk/p_np_5x6_pa1.tsv 0 1 2> chk/p_np_5x6_pa1.err
echo "done py56 exit=$? $(date +%T)" >> runs/census_direct.log
