#!/bin/zsh
# K15 v2 job chain: every job through the shared lock, 1100 s alarm each. Records its own PID in chain.pid.
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/v2
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
run() { # tag, args...
  t=$1; shift
  $H perl -e 'alarm 1100; exec @ARGV' ./grp15 "$@" --out runs/$t > runs/$t.json 2> runs/$t.err
  echo "done $t exit=$?" >> runs/chain.log
}
run np_7x6_f4_32 --nopass --W 7 --H 6 --F 4 --wmax 3 --bmax 2 --sp-variants
run np_8x8_f3_32 --nopass --W 8 --H 8 --F 3 --wmax 3 --bmax 2 --sp-variants
run np_8x8_f4_22 --nopass --W 8 --H 8 --F 4 --wmax 2 --bmax 2 --sp-variants
run tp_8x6_f4_22 --tempo --W 8 --H 6 --F 4 --wmax 2 --bmax 2
run tp_7x6_f3_33 --tempo --W 7 --H 6 --F 3 --wmax 3 --bmax 3
run tp_7x6_f4_22 --tempo --W 7 --H 6 --F 4 --wmax 2 --bmax 2
echo finished >> runs/chain.log
