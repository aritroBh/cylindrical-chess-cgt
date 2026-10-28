#!/bin/zsh
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K20
/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python $D/scripts/check_kg.py cyl:6x6 $D/logs/roots_cyl_6x6.txt "a2" "a3" "a2 b3" "a3 c3" "a2 d2"
