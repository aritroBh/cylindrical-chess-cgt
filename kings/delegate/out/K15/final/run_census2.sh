#!/bin/zsh
# K15 final, part 2: tempo-signature census (independent of the structural classifier) and extensions beyond the brief; every job through the shared lock.
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/final
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
until grep -q repro_finished logs/census.log 2>/dev/null; do sleep 20; done
run() { t=$1; shift
  [[ -s runs/$t.json && -f runs/$t.done ]] && return
  $H perl -e 'alarm 1100; exec @ARGV' ./bin/grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err
  echo "exit=$?" > runs/$t.done; echo "done $t $(date +%T)" >> logs/census.log; }
run tp_7x6_f4_22 --tempo --W 7 --H 6 --F 4 --wmax 2 --bmax 2
run tp_8x6_f4_22 --tempo --W 8 --H 6 --F 4 --wmax 2 --bmax 2
run tp_8x6_f3_33 --tempo --W 8 --H 6 --F 3 --wmax 3 --bmax 3
run tp_7x6_f3_33 --tempo --W 7 --H 6 --F 3 --wmax 3 --bmax 3
for w in 8 7; do h=6
 run npB_${w}x${h}_f5_22 --nopass --W $w --H $h --F 5 --wmax 2 --bmax 2 --sp-variants
 run pA_${w}x${h}_f5_22 --W $w --H $h --F 5 --wmax 2 --bmax 2 --sp-variants
 run npB_${w}x${h}_f4_33 --nopass --W $w --H $h --F 4 --wmax 3 --bmax 3 --sp-variants
 run pA_${w}x${h}_f4_33 --W $w --H $h --F 4 --wmax 3 --bmax 3 --sp-variants
 run npB_${w}x${h}_f3_44 --nopass --W $w --H $h --F 3 --wmax 4 --bmax 4 --sp-variants
 run pA_${w}x${h}_f3_44 --W $w --H $h --F 3 --wmax 4 --bmax 4 --sp-variants
done
echo part2_finished >> logs/census.log
