#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
P=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
$P scripts/R_all.py cyl:8x6 logs/sorties_S.json logs/R_S.json > logs/R_S.log 2>&1
$P scripts/R_all.py cyl:8x6 logs/sorties_k_selected.json logs/R_k.json > logs/R_k.log 2>&1
echo done > logs/R_done
