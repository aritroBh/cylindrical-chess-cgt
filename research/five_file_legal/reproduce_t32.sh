#!/bin/bash
# Reproduce T32 (research/five_file_legal/). Run from anywhere; uses the project's .venv.
#   bash research/five_file_legal/reproduce_t32.sh
# 1. build the C search (cc -O2) into a temporary directory;
# 2. cross-check it against the Python search and the replay checker on small starts;
# 3. covering-model push histories for the 17 positions with a zero-shift assignment (replayed);
# 4. strict pawn-only witness search, ordered mode, S0 only, 120 s per position, two workers
#    (this is the slow step: about 20 minutes). Results land in results_strict_ordered_{A,B}.json.
# Legality, the covering counts and the mirror check are printed by run_t32_c.py as well.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/t32.XXXXXX")"
cc -O2 -o "$WORK/t32_search" research/five_file_legal/t32_search.c
PYTHONPATH=. .venv/bin/python -I research/five_file_legal/crosscheck_c.py "$WORK/t32_search" 2>&1 | head -n 3
PYTHONPATH=. .venv/bin/python -I research/five_file_legal/covering_push.py
(T32_TAGS=S0 T32_ORDERED=1 T32_LOG2=24 T32_NODE_CAP=12000000 T32_TIMEOUT=120 \
 T32_ONLY=1,3,5,7,9,11,13,15,17,19,21 T32_OUT=research/five_file_legal/results_strict_ordered_A.json \
 PYTHONPATH=. .venv/bin/python -I research/five_file_legal/run_t32_c.py "$WORK/t32_search" &)
(T32_TAGS=S0 T32_ORDERED=1 T32_LOG2=24 T32_NODE_CAP=12000000 T32_TIMEOUT=120 \
 T32_ONLY=2,4,6,8,10,12,14,16,18,20 T32_OUT=research/five_file_legal/results_strict_ordered_B.json \
 PYTHONPATH=. .venv/bin/python -I research/five_file_legal/run_t32_c.py "$WORK/t32_search" &)
echo "witness workers started in the background; work dir $WORK"
