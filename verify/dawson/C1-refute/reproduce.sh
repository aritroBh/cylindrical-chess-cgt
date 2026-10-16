#!/bin/sh
# C1-refute reproduce script; run from the project root:
#   sh verify/dawson/C1-refute/reproduce.sh
set -e
D=verify/dawson/C1-refute
cc -O2 -Wall -Wno-unused-function -Wno-unused-but-set-variable -o $D/qverify $D/qverify.c
python3 $D/export_cert.py dawson/quotient_Q32.pkl $D/cert_Q32.txt
$D/qverify $D/cert_Q32.txt > $D/qverify_Q32.txt; tail -3 $D/qverify_Q32.txt      # < 1 s
(cd $D && python3 mutate.py cert_Q32.txt > mutate_Q32.txt)                       # ~1 min
python3 -I $D/brute_misere.py $D/cert_Q32.txt 58 > $D/brute_Q32_T58.txt          # ~1.5 min, ~1 GB RAM
python3 -I $D/pawn_misere.py 12 > $D/pawn_misere_12.txt
