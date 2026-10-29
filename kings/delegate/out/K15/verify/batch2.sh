#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/verify
/usr/bin/time -l ./runcmp.sh cyl86_F4_32_A "--W 8 --H 6 --F 4 --wmax 3 --bmax 2" "--W 8 --H 6 --F 4 --wmax 3 --bmax 2"
/usr/bin/time -l ./runcmp.sh cyl86_F4_32_B "--W 8 --H 6 --F 4 --wmax 3 --bmax 2" "--W 8 --H 6 --F 4 --wmax 3 --bmax 2" nopass
