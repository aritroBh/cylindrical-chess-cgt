#!/bin/bash
# single-component exhaustive scans, small pawn counts: seeds for the search and the <=8-pawn claim
cd "$(dirname "$0")"; mkdir -p small
for spec in "flat 3 3 3" "flat 3 3 4" "flat 3 4 4" "flat 4 3 3" "flat 4 3 4" "flat 4 4 3" "flat 4 4 4" "flat 4 2 5" "flat 4 5 2" "flat 4 3 5" "flat 4 5 3" "flat 5 3 3" "flat 5 3 4" "flat 5 4 3" "flat 5 4 4" "flat 5 3 5" "flat 5 5 3" "flat 5 2 6" "flat 5 6 2" "flat 6 3 3" "flat 6 3 4" "flat 6 4 3" "flat 6 4 4" "flat 6 3 5" "flat 6 5 3" "flat 6 2 6" "flat 6 6 2" "flat 7 4 4" "flat 7 3 5" "flat 7 5 3" "flat 8 4 4" "cyl 3 3 3" "cyl 3 3 4" "cyl 3 4 3" "cyl 3 4 4" "cyl 3 3 5" "cyl 3 5 3" "cyl 4 3 3" "cyl 4 3 4" "cyl 4 4 3" "cyl 4 4 4" "cyl 4 3 5" "cyl 4 5 3" "cyl 5 3 3" "cyl 5 3 4" "cyl 5 4 3" "cyl 5 4 4" "cyl 6 3 3" "cyl 6 3 4" "cyl 6 4 3" "cyl 6 4 4" "cyl 7 4 4" "cyl 7 3 4" "cyl 7 4 3" "cyl 8 4 4"; do
  set -- $spec
  kind=$1; w=$2; nw=$3; nb=$4
  [ $kind = cyl ] && extra="--cylinder" || extra="--flat"
  tag="${kind}_w${w}_${nw}_${nb}"
  nice -n 15 ./s3 $extra --width $w --nw $nw --nb $nb --single > small/$tag.tsv 2> small/$tag.err
  echo "$tag $(tail -1 small/$tag.tsv)"
done
