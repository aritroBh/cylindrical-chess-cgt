#!/bin/zsh
# K15 final: census reruns (reproduction of the earlier attempt's ranges) and extensions; every job through the shared lock.
# usage: run_census.sh <list-name>   (lists below)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/final
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
run() { t=$1; shift
  [[ -s runs/$t.json && -f runs/$t.done ]] && return
  if [[ $t == *8x8* || $t == *f5_32* || $t == *f4_33* || $t == *f3_44* ]]; then
    $H perl -e 'alarm 1100; exec @ARGV' ./bin/grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err
  else
    ( ulimit -t 58; nice -n 15 ./bin/grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err )
  fi
  echo "exit=$?" > runs/$t.done; echo "done $t $(date +%T)" >> logs/census.log; }
case $1 in
 repro)
  for w in 8 7; do h=6
   run pA_${w}x${h}_f3_33 --W $w --H $h --F 3 --wmax 3 --bmax 3 --sp-variants
   run npB_${w}x${h}_f3_33 --nopass --W $w --H $h --F 3 --wmax 3 --bmax 3 --sp-variants
   run pA_${w}x${h}_f4_32 --W $w --H $h --F 4 --wmax 3 --bmax 2 --sp-variants
   run npB_${w}x${h}_f4_32 --nopass --W $w --H $h --F 4 --wmax 3 --bmax 2 --sp-variants
  done
  for w in 7 8; do h=7
   run pA_${w}x${h}_f3_32 --W $w --H $h --F 3 --wmax 3 --bmax 2 --sp-variants
   run npB_${w}x${h}_f3_32 --nopass --W $w --H $h --F 3 --wmax 3 --bmax 2 --sp-variants
  done
  run pA_8x8_f4_22 --W 8 --H 8 --F 4 --wmax 2 --bmax 2 --sp-variants
  run npB_8x8_f4_22 --nopass --W 8 --H 8 --F 4 --wmax 2 --bmax 2 --sp-variants
  run pA_8x8_f3_32 --W 8 --H 8 --F 3 --wmax 3 --bmax 2 --sp-variants
  run npB_8x8_f3_32 --nopass --W 8 --H 8 --F 3 --wmax 3 --bmax 2 --sp-variants
  echo repro_finished >> logs/census.log ;;
 ext)
  for w in 8 7; do h=6
   run pA_${w}x${h}_f5_22 --W $w --H $h --F 5 --wmax 2 --bmax 2 --sp-variants
   run npB_${w}x${h}_f5_22 --nopass --W $w --H $h --F 5 --wmax 2 --bmax 2 --sp-variants
   run pA_${w}x${h}_f3_44 --W $w --H $h --F 3 --wmax 4 --bmax 4 --sp-variants
   run npB_${w}x${h}_f3_44 --nopass --W $w --H $h --F 3 --wmax 4 --bmax 4 --sp-variants
   run pA_${w}x${h}_f4_33 --W $w --H $h --F 4 --wmax 3 --bmax 3 --sp-variants
   run npB_${w}x${h}_f4_33 --nopass --W $w --H $h --F 4 --wmax 3 --bmax 3 --sp-variants
   run pA_${w}x${h}_f5_32 --W $w --H $h --F 5 --wmax 3 --bmax 2 --sp-variants
   run npB_${w}x${h}_f5_32 --nopass --W $w --H $h --F 5 --wmax 3 --bmax 2 --sp-variants
  done
  echo ext_finished >> logs/census.log ;;
esac
