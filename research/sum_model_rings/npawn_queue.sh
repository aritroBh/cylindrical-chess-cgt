#!/bin/zsh
# The n-pawn rings M_10 and O_11 (the least rings *2 on C10 and C11) in the component-sum model, then the C11 RRNR ring
# (O_11 with W5 -> W4) and M_10, O_11 as whole-board games. One process at a time, nice 15.
cd "${0:A:h}/../.."
export PYTHONPATH=.
out=research/sum_model_rings/npawn_values.txt; err=research/sum_model_rings/npawn_values.err
run() { nice -n 15 .venv/bin/python research/ring_family/cyl_run.py "$@" >> $out 2>> $err; }
run "B4 W2 B6 W2 W3 B6 B7 W3 B7 W5"
run "B4 B7 W5 B7 W3 B7 B6 W3 W2 B6 W2"
run "B4 B7 W4 B7 W3 B7 B6 W3 W2 B6 W2" whole
run "B4 W2 B6 W2 W3 B6 B7 W3 B7 W5" whole
run "B4 B7 W5 B7 W3 B7 B6 W3 W2 B6 W2" whole
echo "ALL DONE $(date +%H:%M)" >> $out
