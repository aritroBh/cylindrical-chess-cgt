#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/verify
/usr/bin/time -l nice -n 15 bin/mysolve_t --tempo --W 8 --H 6 --F 4 --wmax 2 --bmax 2 --sigout runs/tempo_c86_F4_22.sig > runs/tempo_c86_F4_22.json 2> runs/tempo_c86_F4_22.err
/usr/bin/time -l nice -n 15 bin/mysolve_t --tempo --W 8 --H 6 --F 3 --wmax 3 --bmax 3 > runs/tempo_c86_F3_33.json 2> runs/tempo_c86_F3_33.err
echo done tempo 8
