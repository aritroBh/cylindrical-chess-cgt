#!/bin/bash
# second-program verification (cylcgt sum + whole, Codex masks) of the new *3 positions; run from the project root
cd "$(dirname "$0")/../.."
PY=.venv/bin/python
V=research/star3_single/verify.py
OUT=research/star4_hunt/out/verify1.txt
: > $OUT
for p in "W: a2 a5 c2 d2 e2 / B: a3 a7 b5 d4 e6" "W: a2 a5 c2 d3 e2 / B: a4 b7 c7 d6 e5" "W: a2 b2 c2 c5 e2 / B: a6 b4 c7 d5 e3"; do
  for m in whole sum; do
    nice -n 15 env PYTHONPATH=. $PY $V $m 5 flat "$p" >> $OUT 2>&1
  done
done
echo "# codex masks" >> $OUT
printf 'W: a2 a5 c2 d2 e2 / B: a3 a7 b5 d4 e6\nW: a2 a5 c2 d3 e2 / B: a4 b7 c7 d6 e5\nW: a2 b2 c2 c5 e2 / B: a6 b4 c7 d5 e3\n' > research/star4_hunt/tmp_v3.txt
nice -n 15 env PYTHONPATH=. $PY research/star3_single/verify_masks.py 5 research/star4_hunt/tmp_v3.txt >> $OUT 2>&1
echo "# rings" >> $OUT
for p in "W: a2 b2 d2 d5 f4 h4 / B: a5 c7 d7 e4 g7 i6" "W: a2 c2 d3 e3 g3 h6 / B: a3 b7 c5 e6 f7 h7"; do
  w=8; echo "$p" | grep -q " i" && w=9
  for m in whole sum; do
    nice -n 15 env PYTHONPATH=. $PY $V $m $w cyl "$p" >> $OUT 2>&1
  done
done
echo VERIFY1DONE >> $OUT
