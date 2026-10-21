#!/bin/sh
# C3 verifier reproduce commands (run from the project root).
# 1. Worker's commands, output redirected here (they only print to stdout).
PYTHONPATH=. .venv/bin/python -m dawson.pawnboard 16 16 > verify/dawson/C3-reproduce/pawnboard_16_rerun.txt
diff verify/dawson/C3-reproduce/pawnboard_16_rerun.txt dawson/pawnboard_16.txt
PYTHONPATH=. .venv/bin/python -m dawson.report_tables > verify/dawson/C3-reproduce/report_tables_rerun.txt
diff verify/dawson/C3-reproduce/report_tables_rerun.txt dawson/report_tables.txt
PYTHONPATH=. .venv/bin/python -u dawson/run_cylcgt_dawson.py 7 > verify/dawson/C3-reproduce/cylcgt_dawson_small_rerun.txt
# 2. Independent C pawn-level solver (verifier's own code).
cc -O2 -Wall -o verify/dawson/C3-reproduce/ringsolve verify/dawson/C3-reproduce/ringsolve.c
verify/dawson/C3-reproduce/ringsolve lemma 3 120 > verify/dawson/C3-reproduce/lemma_3_120.txt
for n in 3 4 5 6 7 8 9 10 11 12 13 14 15 16; do verify/dawson/C3-reproduce/ringsolve solve $n 1 22; done
for n in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16; do verify/dawson/C3-reproduce/ringsolve solve $n 0 22; done
for n in 17 18 19; do verify/dawson/C3-reproduce/ringsolve solve $n 1 24; done
for n in 20 21; do verify/dawson/C3-reproduce/ringsolve solve $n 1 25; done
# 3. Independent Grundy / ring-period / misere-strip check (verifier's own code).
.venv/bin/python -I verify/dawson/C3-reproduce/grundy_check.py > verify/dawson/C3-reproduce/grundy_check.txt
