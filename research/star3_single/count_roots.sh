#!/bin/bash
# root counts (no solving) for candidate single-component scans
cd "$(dirname "$0")"
for spec in "flat 4 4 7" "flat 4 5 6" "flat 4 5 5" "flat 5 4 5" "flat 5 5 5" "flat 5 4 6" "flat 6 4 5" "flat 6 4 4" "flat 7 4 4" "flat 7 3 5" "flat 7 4 5" "flat 8 4 4" "cyl 5 4 5" "cyl 5 5 5" "cyl 4 5 5" "cyl 4 4 5" "cyl 6 5 5" "cyl 7 4 4" "cyl 8 4 4"; do
  set -- $spec
  kind=$1; w=$2; nw=$3; nb=$4
  extra=""; [ $kind = cyl ] && extra="--cylinder" || extra="--flat"
  [ $nw = $nb ] && extra="$extra --colsym"
  nice -n 15 ./s3 $extra --width $w --nw $nw --nb $nb --single --count 2>&1 | tr '\n' ' '
  echo " [$spec]"
done
