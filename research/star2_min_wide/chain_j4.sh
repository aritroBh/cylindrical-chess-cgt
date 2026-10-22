#!/bin/bash
# Codex solver vs cylcgt on every connected part (2..5 pawns)
cd "$(dirname "$0")"
for K in 2 3 4; do PYTHONPATH=../.. nice -n 15 ../../.venv/bin/python check_parts_codex.py $K > codex_parts_k$K.out 2>/dev/null; cat codex_parts_k$K.out | tail -1; done
for R in "0 6200" "6200 12400" "12400 18600" "18600 24722"; do set -- $R
  PYTHONPATH=../.. nice -n 15 ../../.venv/bin/python check_parts_codex.py 5 $1 $2 > codex_parts_k5_$1.out 2>/dev/null; tail -1 codex_parts_k5_$1.out; done
