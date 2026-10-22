#!/bin/bash
# Exhaustive whole-board scan, default setting, every position with <= 8 pawns that has no passed pawn:
#   flat boards of width 1..8 (edge files occupied, interior gaps allowed = sums of components included)
#   rings C3..C8 (all files occupied; a cylinder with an empty file is a flat board).
# Splits nw<=nb only: colour reversal maps (nw,nb) to (nb,nw) and *3 to *3; --colsym when nw==nb.
cd "$(dirname "$0")"; mkdir -p le8
for p in 2 3 4 5 6 7 8; do
 for kind in flat cyl; do
  for w in 1 2 3 4 5 6 7 8; do
   if [ $kind = cyl ] && [ $w -lt 3 ]; then continue; fi
   if [ $kind = cyl ] && [ $p -lt $w ]; then continue; fi   # a ring needs every file occupied
   for nw in 1 2 3 4; do
    nb=$((p-nw)); [ $nb -lt $nw ] && continue
    [ $kind = cyl ] && extra="--cylinder" || extra="--flat"
    [ $nw = $nb ] && extra="$extra --colsym"
    tag="${kind}_w${w}_${nw}_${nb}"
    if [ -f le8/$tag.tsv ] && grep -q "^#summary" le8/$tag.tsv; then echo "$tag (already done)"; continue; fi
    nice -n 15 ./s3 $extra --width $w --nw $nw --nb $nb > le8/$tag.tsv 2> le8/$tag.err
    echo "$tag $(tail -1 le8/$tag.tsv)"
   done
  done
 done
done
