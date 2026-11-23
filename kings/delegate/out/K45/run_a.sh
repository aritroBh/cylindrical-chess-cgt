#!/bin/zsh
# K45 implementation A (K43's table solver, adapted: arbitrary pawn files, 128-bit masks).  Usage: run_a.sh W files
cd "$(dirname $0)"
W=$1; FL=$2; tag=cyl${W}x6_f${FL//,/_}
[[ -f logs/A_$tag.done ]] && exit 0
mkdir logs/A_$tag.claim 2>/dev/null || exit 0
../../heavy.sh ./bin/p45a --kind cyl --W $W --H 6 --files $FL --nw 3 --nb 3 --mode both > logs/A_$tag.out 2> logs/A_$tag.err
echo "rc=$?" > logs/A_$tag.done
