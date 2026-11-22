#!/bin/sh
# For every finished chunk: C1 and C2 per-ring signature files and histograms must be identical.
cd "$(dirname "$0")" || exit 1
for d in results/*.mob1.done; do
  b=${d%.mob1.done}
  [ -f $b.mob2.done ] || { echo "NO C2 $b"; continue; }
  h1=$(zstd -dc -q $b.mob1.sig.zst | cksum); h2=$(zstd -dc -q $b.mob2.sig.zst | cksum)
  o1=$(cksum < $b.mob1.out); o2=$(cksum < $b.mob2.out)
  if [ "$h1" = "$h2" ] && [ "$o1" = "$o2" ]; then echo "AGREE $(basename $b) rings=$(grep RINGS $b.mob1.out | cut -d' ' -f2)"; else echo "DISAGREE $b"; fi
done
