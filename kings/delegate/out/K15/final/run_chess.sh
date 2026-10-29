#!/bin/zsh
# usage: run_chess.sh <board> <inputname> [cap]   -> chess/<board>_<name>_c<cap>.out/.err ; shared lock, own watchdog (3 GB, 1100 s)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/final
b=$1; n=$2; cap=${3:-1}; o=chess/${b//:/_}_${n}_c$cap
[[ -f $o.done ]] && exit 0
/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh ./watch.sh $o.pid 3000000 1100 ./bin/kp --board $b --cap $cap --threads 2 < chess/$n.in > $o.out 2> $o.err
echo "exit=$? $(date +%T)" > $o.done
