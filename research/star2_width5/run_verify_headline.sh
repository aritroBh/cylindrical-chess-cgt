#!/bin/bash
set -u
cd .
N=6
for i in $(seq 0 $((N-1))); do
  PYTHONPATH=. .venv/bin/python research/star2_width5/verify_hits.py --mode headline --chunk "$i" --nchunks "$N" \
      > "research/star2_width5/verify_headline_chunk${i}.log" 2>&1 &
done
wait
echo "headline verification complete"
