#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/f3
run() { t=$1; shift
  ( ulimit -t 100; /usr/bin/time -l nice -n 15 ./grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err )
  echo "done $t exit=$? $(date +%T) $(grep -E 'census done' runs/$t.err | tail -1) rss=$(grep 'maximum resident' runs/$t.err | awk '{print $1}')" >> runs/a88.log; }
run pA_8x8_f3_32 --W 8 --H 8 --F 3 --wmax 3 --bmax 2 --sp-variants
run pA_8x8_f4_22 --W 8 --H 8 --F 4 --wmax 2 --bmax 2 --sp-variants
echo finished >> runs/a88.log
