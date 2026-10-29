#!/bin/zsh
# usage: run_chess2.sh <board> <inputname> <cap> <extra flags...>  -> chess/<board>_<name>_c<cap>_mv.out/.err ; shared lock, watchdog 3 GB / 1100 s
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
b=$1; n=$2; cap=$3; shift 3; o=chess/${b//:/_}_${n}_c${cap}_mv
[[ -f $o.done ]] && exit 0
/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh ./scripts/wd.sh $o.pid 3000000 1100 ./bin/kp --board $b --cap $cap --threads 2 "$@" < chess/$n.in > $o.out 2> $o.err
echo "exit=$? $(date +%T)" > $o.done
