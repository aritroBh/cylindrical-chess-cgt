#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/verify
NP=""; [[ "B" == "B" ]] && NP=nopass
./mine_only.sh c76_F3_44_B "--W 7 --H 6 --F 3 --wmax 4 --bmax 4" $NP
./mine_only.sh c76_F4_33_B "--W 7 --H 6 --F 4 --wmax 3 --bmax 3" $NP
./mine_only.sh c76_F4_42_B "--W 7 --H 6 --F 4 --wmax 4 --bmax 2" $NP
./mine_only.sh c76_F5_32_B "--W 7 --H 6 --F 5 --wmax 3 --bmax 2" $NP
echo done 7 B
