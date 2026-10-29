#!/bin/zsh
# K15 fin2: re-run (own binary built from K15/grp.c) of the census runs of the earlier attempt that fit under one CPU-minute; nice 15, ulimit -t 58 (no lock).
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
run() { t=$1; shift
  [[ -f runs/$t.done ]] && return
  ( ulimit -t 58; nice -n 15 ./bin/grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err )
  echo "exit=$?" > runs/$t.done; echo "done $t $(date +%T)" >> logs/repro.log; }
run flat76_np --flat --W 7 --H 6 --F 3 --wmax 2 --bmax 2 --nopass --sp-variants
for w in 8 7; do h=6
 run pA_${w}x${h}_f3_33 --W $w --H $h --F 3 --wmax 3 --bmax 3 --sp-variants
 run npB_${w}x${h}_f3_33 --nopass --W $w --H $h --F 3 --wmax 3 --bmax 3 --sp-variants
 run pA_${w}x${h}_f4_32 --W $w --H $h --F 4 --wmax 3 --bmax 2 --sp-variants
 run npB_${w}x${h}_f4_32 --nopass --W $w --H $h --F 4 --wmax 3 --bmax 2 --sp-variants
done
echo repro_finished >> logs/repro.log
