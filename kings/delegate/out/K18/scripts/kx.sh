#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python scripts/lg2k.py cyl:8x6 0:3 < logs/k_xcheck_in.txt > logs/k_xcheck_out.txt
