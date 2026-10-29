#!/bin/zsh
# K15 final: boundary censuses, each well under one CPU-minute (ulimit -t 80 as a guard), nice 15, no lock needed.
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/f3
run() { t=$1; shift
  ( ulimit -t 80; nice -n 15 ./grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err )
  echo "done $t exit=$? $(date +%T) $(grep -E 'census done' runs/$t.err | tail -1)" >> runs/census_direct.log; }
run npB_8x6_f3_33 --nopass --W 8 --H 6 --F 3 --wmax 3 --bmax 3 --sp-variants
run npB_7x6_f3_33 --nopass --W 7 --H 6 --F 3 --wmax 3 --bmax 3 --sp-variants
run npB_8x6_f4_32 --nopass --W 8 --H 6 --F 4 --wmax 3 --bmax 2 --sp-variants
run pA_7x6_f3_33 --W 7 --H 6 --F 3 --wmax 3 --bmax 3 --sp-variants
run pA_7x6_f4_32 --W 7 --H 6 --F 4 --wmax 3 --bmax 2 --sp-variants
run pA_8x6_f4_32 --W 8 --H 6 --F 4 --wmax 3 --bmax 2 --sp-variants
echo finished >> runs/census_direct.log
