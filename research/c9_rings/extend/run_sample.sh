#!/bin/bash
# cost sample for an exhaustive C10 / 11-pawn scan: a few enum_rings chunks (round-robin over search prefixes, so
# each chunk is a spread-out sample), solved with the original rg through solve.py (batches of 40).  One process at a time.
cd "$(dirname "$0")"
for job in "5 6 4000 0" "5 6 4000 2001" "4 7 1000 0"; do
  set -- $job
  tag=s$1_$2_c$4of$3
  nice -n 15 ../enum_rings 10 11 $1 $2 --chunk $4 $3 > sample/$tag.rings 2> sample/$tag.enum.err
  awk '{print $0 "\t" "sample"}' sample/$tag.rings > sample/$tag.cand.tsv
  rm -f sample/$tag.res.tsv sample/$tag.res.tsv.log
  s=$(date +%s)
  nice -n 15 python3 solve.py sample/$tag.cand.tsv sample/$tag.res.tsv
  e=$(date +%s)
  echo "$tag rings $(wc -l < sample/$tag.rings) wall_s=$((e-s))" >> sample/summary.txt
  rm -f sample/$tag.cand.tsv
done
echo done >> sample/summary.txt
