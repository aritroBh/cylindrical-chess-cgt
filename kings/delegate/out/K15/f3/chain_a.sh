#!/bin/zsh
# K15 final: boundary census runs, every job through the shared lock, 1100 s alarm each.
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/f3
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
run() { t=$1; shift
  $H perl -e 'alarm 1100; exec @ARGV' ./grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err
  echo "done $t exit=$? $(date +%T)" >> runs/chain_a.log; }
run npB_8x6_f3_33 --nopass --W 8 --H 6 --F 3 --wmax 3 --bmax 3 --sp-variants
run npB_7x6_f3_33 --nopass --W 7 --H 6 --F 3 --wmax 3 --bmax 3 --sp-variants
run npB_8x6_f4_32 --nopass --W 8 --H 6 --F 4 --wmax 3 --bmax 2 --sp-variants
run pA_7x6_f3_33 --W 7 --H 6 --F 3 --wmax 3 --bmax 3 --sp-variants
run pA_7x6_f4_32 --W 7 --H 6 --F 4 --wmax 3 --bmax 2 --sp-variants
run pA_8x6_f4_32 --W 8 --H 6 --F 4 --wmax 3 --bmax 2 --sp-variants
echo finished >> runs/chain_a.log
