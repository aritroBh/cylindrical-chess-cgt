#!/bin/bash
cd "$(dirname "$0")"
for spec in "flat 6 3 6" "flat 6 2 7" "flat 7 3 6" "flat 7 2 7" "cyl 5 5 5" "cyl 6 5 5" "cyl 6 4 5" "flat 8 4 5"; do
  set -- $spec
  [ $1 = cyl ] && extra="--cylinder" || extra="--flat"
  [ $3 = $4 ] && extra="$extra --colsym"
  nice -n 15 ./s3 $extra --width $2 --nw $3 --nb $4 --single --count 2>&1 | head -1 | sed "s/ chunk=0\/1//" | tr '\n' ' '
  echo "[$spec]"
done
