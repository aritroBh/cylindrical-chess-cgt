#!/bin/zsh
# K44 item 3: faithful configurations in the P model (first promotion wins, real kings): ref3m (K23 referee solver) and kp_p --pmodel (K7)
D=$(cd "$(dirname "$0")/.." && pwd)
cd $D
( ulimit -t 3000; /usr/bin/time -p bin/ref3m --board cyl:7x6 < tmp/p7.pos > logs/p7.ref3 2> logs/p7.ref3.err )
( ulimit -t 3000; /usr/bin/time -p bin/ref3m --board cyl:8x6 < tmp/p8.pos > logs/p8.ref3 2> logs/p8.ref3.err )
( ulimit -t 1500; /usr/bin/time -p bin/kp_p --board cyl:10x6 --pmodel --cap 1 --threads 1 < tmp/o2.pos > logs/o2.kpp 2> logs/o2.kpp.err )
( ulimit -t 3000; /usr/bin/time -p bin/kp_p --board cyl:7x6 --pmodel --cap 1 --threads 1 < tmp/p7.pos > logs/p7.kpp 2> logs/p7.kpp.err )
echo done > logs/run_p.done
