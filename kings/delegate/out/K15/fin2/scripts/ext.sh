#!/bin/zsh
# K15 fin2: the larger census runs, every job through the shared lock (heavy.sh), own RSS/wall watchdog (3 GB, 1100 s).
# usage: ext.sh <set>   set = repro2 (re-run of the earlier attempt's larger runs) | new (runs beyond the earlier attempt)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
run() { t=$1; shift
  [[ -f runs/$t.done ]] && return
  $H ./scripts/wd.sh runs/$t.pid 3000000 1100 ./bin/grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err
  echo "exit=$?" > runs/$t.done; echo "done $t $(date +%T)" >> logs/ext.log; }
case $1 in
 repro2)
  for w in 8 7; do h=6
   run pA_${w}x${h}_f5_22 --W $w --H $h --F 5 --wmax 2 --bmax 2 --sp-variants
   run npB_${w}x${h}_f5_22 --nopass --W $w --H $h --F 5 --wmax 2 --bmax 2 --sp-variants
   run pA_${w}x${h}_f3_44 --W $w --H $h --F 3 --wmax 4 --bmax 4 --sp-variants
   run npB_${w}x${h}_f3_44 --nopass --W $w --H $h --F 3 --wmax 4 --bmax 4 --sp-variants
   run pA_${w}x${h}_f4_33 --W $w --H $h --F 4 --wmax 3 --bmax 3 --sp-variants
   run npB_${w}x${h}_f4_33 --nopass --W $w --H $h --F 4 --wmax 3 --bmax 3 --sp-variants
  done
  for w in 7 8; do h=7
   run pA_${w}x${h}_f3_32 --W $w --H $h --F 3 --wmax 3 --bmax 2 --sp-variants
   run npB_${w}x${h}_f3_32 --nopass --W $w --H $h --F 3 --wmax 3 --bmax 2 --sp-variants
  done
  run pA_8x8_f4_22 --W 8 --H 8 --F 4 --wmax 2 --bmax 2 --sp-variants
  run npB_8x8_f4_22 --nopass --W 8 --H 8 --F 4 --wmax 2 --bmax 2 --sp-variants
  run pA_8x8_f3_32 --W 8 --H 8 --F 3 --wmax 3 --bmax 2 --sp-variants
  run npB_8x8_f3_32 --nopass --W 8 --H 8 --F 3 --wmax 3 --bmax 2 --sp-variants
  echo repro2_finished >> logs/ext.log ;;
 new)
  run flatA_7x6_f3_22 --flat --W 7 --H 6 --F 3 --wmax 2 --bmax 2 --sp-variants
  run flatA_7x6_f3_33 --flat --W 7 --H 6 --F 3 --wmax 3 --bmax 3 --sp-variants
  run flatB_7x6_f3_33 --flat --nopass --W 7 --H 6 --F 3 --wmax 3 --bmax 3 --sp-variants
  for w in 8 7; do h=6
   run pA_${w}x${h}_f5_32 --W $w --H $h --F 5 --wmax 3 --bmax 2 --sp-variants
   run npB_${w}x${h}_f5_32 --nopass --W $w --H $h --F 5 --wmax 3 --bmax 2 --sp-variants
   run pA_${w}x${h}_f4_42 --W $w --H $h --F 4 --wmax 4 --bmax 2 --sp-variants
   run npB_${w}x${h}_f4_42 --nopass --W $w --H $h --F 4 --wmax 4 --bmax 2 --sp-variants
  done
  echo new_finished >> logs/ext.log ;;
esac
