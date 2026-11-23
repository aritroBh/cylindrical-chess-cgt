#!/bin/sh
# compare.sh basename-in-results [oldbase]: mob1 vs mob2 per-ring sigs and .out identical
cd "$(dirname "$0")/results" || exit 1
b=$1
h1=$(zstd -dc -q $b.mob1.sig.zst | cksum); h2=$(zstd -dc -q $b.mob2.sig.zst | cksum)
o1=$(cksum < $b.mob1.out); o2=$(cksum < $b.mob2.out)
if [ "$h1" = "$h2" ] && [ "$o1" = "$o2" ]; then echo "AGREE $b rings=$(grep RINGS $b.mob1.out | cut -d' ' -f2) hits=$(grep -c HIT $b.mob1.out)"; else echo "DISAGREE $b"; fi
