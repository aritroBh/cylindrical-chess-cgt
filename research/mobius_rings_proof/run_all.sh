#!/bin/sh
# Reruns every finite check of PROOF.md, one process at a time, under nice 15 (about 6 minutes on the author's machine).
# Run from anywhere; writes logs/ next to this script.
cd "$(dirname "$0")" || exit 1
for f in F1 F2 F3; do nice -n 15 python3 verify.py $f 0 13 > logs/verify_$f.log 2>&1; done
nice -n 15 python3 verify.py F1 5 7 --cyl > logs/verify_F1_cylinder_control.log 2>&1
(for f in F1 F2 F3; do nice -n 15 python3 seam_moves.py $f 5; done) > logs/seam_moves.log 2>&1
nice -n 15 python3 base.py > logs/base.log 2>&1
nice -n 15 python3 difftest.py 7 3000 > logs/difftest_7_3000.log 2>&1
nice -n 15 python3 difftest_cover.py 7 3000 > logs/difftest_cover_7_3000.log 2>&1
nice -n 15 python3 lemma_test.py 3 3000 > logs/lemma_test_3_3000.log 2>&1
