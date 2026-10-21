#!/bin/sh
# All settings, <= 5 pawns. Run from verify/cylatlas/C5-refute.
PY=../../../.venv/bin/python
for split in 1 0; do
 for ep in 1 0; do
  for rule in count mover opponent; do
   $PY scan.py --rule $rule --ep $ep --epaware 0 --split $split --maxp 5 --out scan5_${rule}_ep${ep}_aw0_split${split}.json > log_${rule}_ep${ep}_aw0_split${split}.txt 2>&1
  done
 done
 for rule in count mover opponent; do
   $PY scan.py --rule $rule --ep 1 --epaware 1 --split $split --maxp 5 --out scan5_${rule}_ep1_aw1_split${split}.json > log_${rule}_ep1_aw1_split${split}.txt 2>&1
 done
done
echo DONE
