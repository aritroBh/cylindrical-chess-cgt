#!/bin/sh
cd "$(dirname "$0")"
run() { nice -n 10 python3 hunt.py "$@" >> batch1.log 2>&1; }
run 101 6000 cyl:7x6 0,1,2 5 3 0.7 any a1
run 102 6000 cyl:7x6 1,2,3 5 3 0.7 any a2
run 103 6000 cyl:7x6 0,1 5 3 0.7 any a3
run 104 6000 cyl:7x6 0,1,2,3 5 3 0.7 any a4
run 105 6000 cyl:7x5 0,1,2 4 3 0.7 any a5
run 106 6000 flat:6x6 0,1,2 5 3 0.7 any a6
run 107 6000 flat:6x6 1,2 5 3 0.7 any a7
run 108 6000 flat:7x6 2,3,4 5 3 0.7 any a8
run 109 6000 cyl:6x6 0,1 5 3 0.7 any a9
echo done > batch1.done
