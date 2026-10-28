#!/bin/zsh
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K20
P=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
$P $D/scripts/check_kg.py cyl:7x6 $D/logs/roots_cyl_7x6.txt "a2 c3" "a3 c4"
$P $D/scripts/check_kg.py cyl:8x6 $D/logs/roots_cyl_8x6.txt "a3" "a2 d3"
$P $D/scripts/check_kg.py flat:6x6 $D/logs/roots_flat_6x6.txt "a4 c2" "a2 d4" "b2" "a2 b3" "a3 c3"
