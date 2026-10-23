#!/bin/bash
# dense small-width exhaustive scans (single-component roots): cylinders C3, C4 and flat w3, w4
cd "$(dirname "$0")"
source ./scanlib.sh
# rings C3: pawns 11..14 (splits nw<=nb)
for sp in "5 6" "4 7" "3 8" "2 9"; do set -- $sp; scan c3p11 cylinder 3 $1 $2 2; done
for sp in "6 6" "5 7" "4 8" "3 9"; do set -- $sp; if [ $1 -eq $2 ]; then scan c3p12 cylinder 3 $1 $2 2 --colsym; else scan c3p12 cylinder 3 $1 $2 2; fi; done
for sp in "6 7" "5 8" "4 9"; do set -- $sp; scan c3p13 cylinder 3 $1 $2 2; done
# rings C4: pawns 11 and 12
scan c4p11 cylinder 4 4 7 4
scan c4p11 cylinder 4 5 6 6
scan c4p11 cylinder 4 3 8 2
scan c4p12 cylinder 4 6 6 8 --colsym
scan c4p12 cylinder 4 5 7 8
scan c4p12 cylinder 4 4 8 4
# flat w4: pawns 11 and 12
scan w4p11 flat 4 3 8 4
scan w4p11 flat 4 4 7 8
scan w4p11 flat 4 5 6 12
scan w4p12 flat 4 4 8 8
scan w4p12 flat 4 5 7 16
scan w4p12 flat 4 6 6 12 --colsym
echo ALLDONE > logs/queue8.done
