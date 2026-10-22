#!/bin/sh
cd "$(dirname "$0")"
while [ ! -f batch3.done ]; do sleep 20; done
runa() { nice -n 10 python3 hunt_a.py "$@" >> batch4.log 2>&1; }
runa 411 6000 cyl:7x6 0,1,2 4 3 0.5 z1
runa 412 6000 flat:6x6 0,1,2 4 3 0.5 z2
runa 413 6000 cyl:7x6 1,2,3 4 3 0.5 z3
runa 414 6000 flat:7x6 2,3,4 4 3 0.5 z4
echo done > batch4.done
