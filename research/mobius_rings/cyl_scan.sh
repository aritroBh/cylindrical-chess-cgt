#!/bin/sh
# usage: cyl_scan.sh N P   -- cylinder C_N with P pawns (all colour splits, enum_rings classes, colours not exchanged),
# solved by rg_copy (h = 0..3); prints the signature histogram.  One worker.
cd "$(dirname "$0")" || exit 1
n=$1; p=$2; nw=1
while [ $nw -lt $p ]; do
  ../c9_rings/enum_rings $n $p $nw $((p-nw)) 2>/dev/null
  nw=$((nw+1))
done | nice -n 15 ../c9_rings/rg_copy solve 3 | awk '{print $1}' | sort | uniq -c | sort -rn | awk -v n=$n -v p=$p '{print "CYL n=" n " P=" p " " $2 " " $1}'
