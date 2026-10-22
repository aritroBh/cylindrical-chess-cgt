#!/bin/sh
cd "$(dirname "$0")"
run() { nice -n 10 python3 hunt_ep2.py "$@" >> batch5.log 2>&1; }
run 255 4000 cyl:7x5 0,1,2 4 c5
run 258 4000 cyl:6x6 0,1 5 c8
run 257 3000 cyl:8x6 0,1,2 5 c7
run 256 3000 cyl:7x7 0,1,2 5 c6
echo done > batch5.done
