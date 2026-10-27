#!/bin/zsh
# Exhaustive scan of the local game (no promotion clause, then --safe), through the shared heavy lock.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
run() { name=$1; shift; echo "== $name: $*" >> $D/logs/scan_progress.txt; $H $D/local "$@" > $D/logs/scan_$name.txt 2>&1; echo "done $name rc=$?" >> $D/logs/scan_progress.txt; }
run flat5x6_w3b3     --board flat 5 6 --fz 0 4 enum --f 2 --wmax 3 --bmax 3 --ep --ex 10
run flat5x6_w3b3_safe --board flat 5 6 --fz 0 4 --safe enum --f 2 --wmax 3 --bmax 3 --ep --ex 10
