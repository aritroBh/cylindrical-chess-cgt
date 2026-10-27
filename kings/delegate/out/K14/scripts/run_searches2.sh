#!/bin/bash
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K14
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
$H $PY scripts/search_groups.py flat:7x6 3 2 2 18 > logs/c2_flat7x6_fz3_22.jsonl 2> logs/c2_flat7x6_fz3_22.err
$H $PY scripts/search_groups.py flat:7x6 2 3 3 18 > logs/c2_flat7x6_fz2_33.jsonl 2> logs/c2_flat7x6_fz2_33.err
$H $PY scripts/search_groups.py cyl:7x6 3 2 2 18 > logs/c2_cyl7x6_fz3_22.jsonl 2> logs/c2_cyl7x6_fz3_22.err
$H $PY scripts/search_groups.py flat:7x6 3 3 3 14 > logs/c2_flat7x6_fz3_33.jsonl 2> logs/c2_flat7x6_fz3_33.err
