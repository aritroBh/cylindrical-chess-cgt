#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
P=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
$P scripts/lg2.py --board cyl:8x6 --fz 0:3 < logs/rand_8x6_a.txt > logs/rand_8x6_a.py
$P scripts/lg2.py --board cyl:7x6 --fz 0:3 < logs/rand_7x6_a.txt > logs/rand_7x6_a.py
