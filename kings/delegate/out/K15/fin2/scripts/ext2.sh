#!/bin/zsh
# K15 fin2: tempo-signature census (independent of the structural classifier), through the shared lock, 3 GB / 1100 s watchdog.
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
until grep -q new_finished logs/ext.log 2>/dev/null; do sleep 30; done
run() { t=$1; shift
  [[ -f runs/$t.done ]] && return
  $H ./scripts/wd.sh runs/$t.pid 3000000 1100 ./bin/grp "$@" --out runs/$t > runs/$t.json 2> runs/$t.err
  echo "exit=$?" > runs/$t.done; echo "done $t $(date +%T)" >> logs/ext2.log; }
run tp_7x6_f4_22 --tempo --W 7 --H 6 --F 4 --wmax 2 --bmax 2
run tp_8x6_f4_22 --tempo --W 8 --H 6 --F 4 --wmax 2 --bmax 2
run tp_7x6_f3_33 --tempo --W 7 --H 6 --F 3 --wmax 3 --bmax 3
run tp_8x6_f3_33 --tempo --W 8 --H 6 --F 3 --wmax 3 --bmax 3
run tp_7x6_f5_22 --tempo --W 7 --H 6 --F 5 --wmax 2 --bmax 2
run tp_8x6_f5_22 --tempo --W 8 --H 6 --F 5 --wmax 2 --bmax 2
run tp_7x6_f4_32 --tempo --W 7 --H 6 --F 4 --wmax 3 --bmax 2
echo tempo_finished >> logs/ext2.log
