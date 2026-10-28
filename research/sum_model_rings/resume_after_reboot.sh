#!/bin/zsh
# Jobs cut by the 2026-10-27 20:43 reboot: Qo_11 as a sum (its whole-board value, *3, finished before the reboot),
# then the C14 sum value (run.sh, 4th ring).
cd "${0:A:h}/../.."
export PYTHONPATH=.
nice -n 15 .venv/bin/python research/ring_family/cyl_run.py "W4 B7 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4" >> research/sum_model_rings/odd_values.txt 2>> research/sum_model_rings/odd_values.err
echo "ALL DONE $(date +%H:%M)" >> research/sum_model_rings/odd_values.txt
nice -n 15 .venv/bin/python research/ring_family/cyl_run.py "B5 W2B5 W35B6 W2 B4 W2 B4 W2 B4 W2 B4 W2 B4 W2" >> research/sum_model_rings/sum_values.txt 2>> research/sum_model_rings/sum_values.err
echo "ALL DONE $(date +%H:%M)" >> research/sum_model_rings/sum_values.txt
