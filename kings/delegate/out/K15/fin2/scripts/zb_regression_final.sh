#!/bin/zsh
# Z_B regression test on flat 7x6 (all four king states): one-ply classifier of the brief (oneply.py), exact classifier (grp, plain P and with passes), kp_p move lists.
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
echo "### one-ply classifier (brief's tests; scripts/oneply.py), flat 7x6, F_Z = a-c"
nice -n 15 python3 scripts/oneply.py --flat --W 7 --H 6 --F 3 "Kb2 ka4 Pa3 Pb4 pb3 pc4" "Kb2 kb5 Pa3 Pb4 pb3 pc4" "Kc3 ka4 Pa3 Pb4 pb3 pc4" "Kc3 kb5 Pa3 Pb4 pb3 pc4" | grep -E "^==|label"
for md in nopass pass; do
  echo; echo "### exact classifier grp, reading $md (B = plain P, A = free passes), flat 7x6, 3 files, <= 2+2 pawns, root passers allowed"
  flag=""; [[ $md == nopass ]] && flag="--nopass"
  for p in "Kb2 ka4 Pa3 Pb4 pb3 pc4 w -" "Kb2 kb5 Pa3 Pb4 pb3 pc4 w -" "Kc3 ka4 Pa3 Pb4 pb3 pc4 w -" "Kc3 kb5 Pa3 Pb4 pb3 pc4 w -"; do
    nice -n 15 ./bin/grp --flat --W 7 --H 6 --F 3 --wmax 2 --bmax 2 $flag --classify "$p" 2>&1 | grep -E "^(==|class|safe [WB]=)"
  done
done
