#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/verify
NP=""; [[ "B" == "B" ]] && NP=nopass
./mine_only.sh c88_F4_22_B "--W 8 --H 8 --F 4 --wmax 2 --bmax 2" $NP
./mine_only.sh c88_F3_32_B "--W 8 --H 8 --F 3 --wmax 3 --bmax 2" $NP
echo done 88 B
