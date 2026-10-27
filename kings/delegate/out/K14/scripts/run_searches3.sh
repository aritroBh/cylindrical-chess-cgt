#!/bin/bash
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K14
/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python scripts/search_groups.py flat:7x6 2 3 3 18 > logs/c2_flat7x6_fz2_33.jsonl 2> logs/c2_flat7x6_fz2_33.err
/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python scripts/search_groups.py flat:7x6 3 3 3 12 > logs/c2_flat7x6_fz3_33.jsonl 2> logs/c2_flat7x6_fz3_33.err
