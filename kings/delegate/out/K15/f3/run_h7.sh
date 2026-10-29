#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/f3
run() { t=$1; shift
  ( ulimit -t 90; /usr/bin/time -l nice -n 15 ./grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err )
  echo "done $t exit=$? $(date +%T) $(grep -E 'census done' runs/$t.err | tail -1) rss=$(grep 'maximum resident' runs/$t.err | awk '{print $1}')" >> runs/h7.log; }
run pA_7x7_f3_32 --W 7 --H 7 --F 3 --wmax 3 --bmax 2 --sp-variants
run npB_7x7_f3_32 --nopass --W 7 --H 7 --F 3 --wmax 3 --bmax 2 --sp-variants
run pA_8x7_f3_32 --W 8 --H 7 --F 3 --wmax 3 --bmax 2 --sp-variants
run npB_8x7_f3_32 --nopass --W 8 --H 7 --F 3 --wmax 3 --bmax 2 --sp-variants
echo finished >> runs/h7.log
