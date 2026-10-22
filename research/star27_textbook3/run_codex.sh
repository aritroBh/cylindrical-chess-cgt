#!/bin/sh
# T27 step 3: run the independent whole-board solver (verify_ext/codex/solver.py) on every position whose
# scanner cell is "N,3".  Usage (project root):
#   sh research/star27_textbook3/run_codex.sh RACE EP PASSED SCANNER_COL [LIMIT] > out.tsv
#     RACE = count|mover|opponent   EP = on|off   PASSED = textbook|aware
#     SCANNER_COL = column of scanner_rows.tsv that selects the positions: 4 C/T, 5 C/off, 6 C/aware, 7 M/T, 8 M/off, 9 M/aware
#     LIMIT = optional: only the first LIMIT positions
# Each run is one process under nice; the 4 positions with a b-file pawn take 5-9 minutes each, the rest seconds.
D=research/star27_textbook3
awk -F'\t' -v c="$4" '$c == "N,3" {print $1}' $D/scanner_rows.tsv | head -n "${5:-1000}" | tr '\n' '\0' |
  xargs -0 env PYTHONPATH=. nice -n 10 .venv/bin/python $D/verify_codex.py "$1" "$2" "$3"
