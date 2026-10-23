#!/bin/bash
cd /Users/aritro/Downloads/Research/Chessendgames
R=/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k10/fin/realk.py
for a in "6 6 2 2" "7 6 2 2"; do echo "== $a"; PYTHONPATH=. nice -n 10 .venv/bin/python $R $a 2>&1 | tail -3 | cut -c1-1800; done
