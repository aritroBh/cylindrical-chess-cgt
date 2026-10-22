#!/bin/bash
# re-run, with the table capped at 2^25 entries (1.9 GB), the three 8-pawn scans that originally ran uncapped
cd "$(dirname "$0")"
for spec in "7 4 4" "8 3 5" "8 4 4"; do
  set -- $spec
  extra="--flat"; [ $2 = $3 ] && extra="--flat --colsym"
  nice -n 15 ./s3 $extra --width $1 --nw $2 --nb $3 --max-entries 33554432 > le8_capped/flat_w$1_$2_$3.tsv 2> le8_capped/flat_w$1_$2_$3.err
  echo "flat_w$1_$2_$3 $(tail -1 le8_capped/flat_w$1_$2_$3.tsv)"
done
