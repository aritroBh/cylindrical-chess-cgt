#!/bin/zsh
# Sum-of-components values (cylcgt default model) of rings proved *2/*3 only as whole-board games.
# One process, nice 15, sequential; results appended to sum_values.txt. Run from anywhere.
cd "${0:A:h}/../.."
for r in "W5 B7 W4 W4B7 B6 W3B6 W2 B4 W2 B4" \
         "W4 B7 B4 W2 W3B6 W3 W2B5 B5 W2 B4" \
         "W23B4 B5 W2B5 W3 B5 W3 B5 W3 B5 W3 B5 W3 B5" \
         "B5 W2B5 W35B6 W2 B4 W2 B4 W2 B4 W2 B4 W2 B4 W2"; do
  nice -n 15 .venv/bin/python research/ring_family/cyl_run.py "$r" >> research/sum_model_rings/sum_values.txt 2>> research/sum_model_rings/sum_values.err
done
echo "ALL DONE $(date +%H:%M)" >> research/sum_model_rings/sum_values.txt
