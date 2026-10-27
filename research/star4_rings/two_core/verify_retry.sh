#!/bin/sh
# one position per call, original rg, TBITS=24
i=0
while read -r line; do
  i=$((i+1))
  out=$(echo "$line" | TBITS=24 nice -n 15 ./rg solve 7 2>&1 | head -1)
  echo "$i $out"
done < verify_retry_in.txt
