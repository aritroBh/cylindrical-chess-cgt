#!/bin/zsh
# K15 fin2: leaner census queue.  Part U: runs under one CPU-minute (ulimit -t 58, nice 15, no lock).  Part L: the rest, through the shared lock with the watchdog.
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
runU() { t=$1; shift
  [[ -f runs/$t.done ]] && return
  ( ulimit -t 58; nice -n 15 ./bin/grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err )
  echo "exit=$?" > runs/$t.done; echo "done $t $(date +%T)" >> logs/ext3.log; }
runL() { t=$1; shift
  [[ -f runs/$t.done ]] && return
  $H ./scripts/wd.sh runs/$t.pid 3000000 1100 ./bin/grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err
  echo "exit=$?" > runs/$t.done; echo "done $t $(date +%T)" >> logs/ext3.log; }
case $1 in
 U)
  for w in 8 7; do h=6
   runU pA_${w}x${h}_f5_22 --W $w --H $h --F 5 --wmax 2 --bmax 2 --sp-variants
   runU npB_${w}x${h}_f5_22 --nopass --W $w --H $h --F 5 --wmax 2 --bmax 2 --sp-variants
  done
  runU tp_7x6_f4_22 --tempo --W 7 --H 6 --F 4 --wmax 2 --bmax 2
  runU tp_8x6_f4_22 --tempo --W 8 --H 6 --F 4 --wmax 2 --bmax 2
  echo U_finished >> logs/ext3.log ;;
 L)
  for w in 8 7; do h=6
   runL pA_${w}x${h}_f5_32 --W $w --H $h --F 5 --wmax 3 --bmax 2 --sp-variants
   runL npB_${w}x${h}_f5_32 --nopass --W $w --H $h --F 5 --wmax 3 --bmax 2 --sp-variants
   runL pA_${w}x${h}_f4_42 --W $w --H $h --F 4 --wmax 4 --bmax 2 --sp-variants
   runL npB_${w}x${h}_f4_42 --nopass --W $w --H $h --F 4 --wmax 4 --bmax 2 --sp-variants
  done
  runL flatA_7x6_f3_33 --flat --W 7 --H 6 --F 3 --wmax 3 --bmax 3 --sp-variants
  runL flatB_7x6_f3_33 --flat --nopass --W 7 --H 6 --F 3 --wmax 3 --bmax 3 --sp-variants
  runL flatA_7x6_f3_22 --flat --W 7 --H 6 --F 3 --wmax 2 --bmax 2 --sp-variants
  runL tp_7x6_f3_33 --tempo --W 7 --H 6 --F 3 --wmax 3 --bmax 3
  runL tp_8x6_f3_33 --tempo --W 8 --H 6 --F 3 --wmax 3 --bmax 3
  for w in 7 8; do h=6
   runL pA_${w}x${h}_f3_44 --W $w --H $h --F 3 --wmax 4 --bmax 4 --sp-variants
   runL npB_${w}x${h}_f3_44 --nopass --W $w --H $h --F 3 --wmax 4 --bmax 4 --sp-variants
  done
  echo L_finished >> logs/ext3.log ;;
esac
