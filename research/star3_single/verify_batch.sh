#!/bin/bash
# cylcgt (sum model and whole-board model) for one representative of each *3 class not yet checked, then Codex masks
cd "$(dirname "$0")/../.."
export PYTHONPATH=.
V=research/star3_single/verify.py
run() { nice -n 15 .venv/bin/python $V "$1" "$2" flat "$3"; }
for spec in \
 "5|W: a4 b3 d2 d3 e5 / B: a7 b7 c5 e7" \
 "5|W: a2 b4 c3 e2 e3 / B: a4 b7 c7 d5" \
 "6|W: a2 b2 c4 f2 / B: a5 b6 d6 d7 e5" \
 "6|W: a2 b2 c4 e3 / B: a5 b6 d6 d7 f6" \
 "6|W: a2 b2 c4 e2 / B: a5 b6 d6 d7 f5" \
 "6|W: a4 c2 d2 e4 / B: b7 c5 d6 f6 f7" ; do
  w=${spec%%|*}; pos=${spec#*|}
  run sum $w "$pos"
  run whole $w "$pos"
done
