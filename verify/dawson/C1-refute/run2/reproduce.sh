#!/bin/sh
# C1-refute run2 (fresh, independent of the earlier files in ../); run from the project root:
#   sh verify/dawson/C1-refute/run2/reproduce.sh
set -e
D=verify/dawson/C1-refute/run2
python3 -I $D/export.py dawson/quotient_Q32.pkl $D/cert_Q32.txt         # data only, no worker code
cc -O2 -Wall -o $D/qcheck $D/qcheck.c
$D/qcheck $D/cert_Q32.txt > $D/qcheck_Q32.txt; tail -2 $D/qcheck_Q32.txt # ~1 s: full proof
python3 -I $D/mutants.py $D/cert_Q32.txt > $D/mutants_Q32.txt            # ~8 min under load
python3 -I $D/brute.py $D/cert_Q32.txt 56 > $D/brute_T56.txt             # ~2 min
python3 -I $D/pawns_misere.py $D/cert_Q32.txt 15 > $D/pawns_misere_15.txt  # ~10 s
pdftotext -layout verify/dawson/C1-reproduce/lit/ps_0609825v5.pdf $D/lit/ps_from_pdf.txt
grep -n "Q33 (0.07) has order" $D/lit/ps_from_pdf.txt
