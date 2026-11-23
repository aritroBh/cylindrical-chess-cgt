#!/bin/zsh
D=$(cd "$(dirname "$0")/.." && pwd)
cd $D
( ulimit -t 3000; /usr/bin/time -p bin/ref3m --board cyl:7x6 < tmp/p7n.pos > logs/p7n.ref3 2> logs/p7n.ref3.err )
echo done > logs/run_p3.done
