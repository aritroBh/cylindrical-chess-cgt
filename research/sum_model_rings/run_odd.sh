#!/bin/zsh
# cylcgt values of the odd n+2 rings R_11 (*2) and Qo_11 (*3), whole-board then sum; sequential, nice 15.
cd "${0:A:h}/../.."
for r in "W5 B7 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4" "W4 B7 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4"; do
  for m in whole sum; do
    nice -n 15 .venv/bin/python research/ring_family/cyl_run.py "$r" $([[ $m == whole ]] && echo whole) >> research/sum_model_rings/odd_values.txt 2>> research/sum_model_rings/odd_values.err
  done
done
echo "ALL DONE $(date +%H:%M)" >> research/sum_model_rings/odd_values.txt
