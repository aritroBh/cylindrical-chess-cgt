#!/bin/zsh
D=$(cd "$(dirname "$0")/.." && pwd)
cd $D
( ulimit -t 1500; /usr/bin/time -p bin/kp_p10 --board cyl:10x6 --pmodel --cap 1 --threads 1 < tmp/o2.pos > logs/o2.kpp 2> logs/o2.kpp.err )
( ulimit -t 3000; /usr/bin/time -p bin/kp_p --board cyl:8x6 --pmodel --cap 1 --threads 1 < tmp/p8.pos > logs/p8.kpp 2> logs/p8.kpp.err )
echo done > logs/run_p2.done
