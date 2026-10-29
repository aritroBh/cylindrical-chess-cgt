#!/bin/zsh
# builds logs/test_cap1.in (<= 1 officer incl. pawns' promotions possible) and logs/test_cap2.in from the generated position files
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K28/logs
cat t_1p0o.in t_0p1o.in t_2p0o.in t_2p0o_race.in t_1p1o.in t_1p1o_race.in valmoves1.in | sort -u > test_cap1.in
cat t_0p2o.in t_1p1o.in t_1p1o_race.in t_2p0o.in t_2p0o_race.in | sort -u > test_exact2.in
wc -l test_cap1.in test_exact2.in
