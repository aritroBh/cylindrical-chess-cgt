#!/bin/sh
cd "$(dirname "$0")"
run() { nice -n 10 python3 hunt_ep2.py "$@" >> batch2.log 2>&1; }
run 201 5000 cyl:7x6 0,1,2 5 b1
run 202 5000 cyl:7x6 1,2,3 5 b2
run 203 5000 flat:6x6 0,1,2 5 b3
run 204 5000 flat:7x6 2,3,4 5 b4
run 205 5000 cyl:7x5 0,1,2 4 b5
run 206 4000 cyl:7x7 0,1,2 5 b6
run 207 5000 cyl:8x6 0,1,2 5 b7
run 208 5000 cyl:6x6 0,1 5 b8
echo done > batch2.done
