#!/bin/sh
cd "$(dirname "$0")"
while [ ! -f batch1.done ]; do sleep 20; done
runa() { nice -n 10 python3 hunt_a.py "$@" >> batch3.log 2>&1; }
runs() { nice -n 10 python3 hunt_st.py "$@" >> batch3.log 2>&1; }
rune() { nice -n 10 python3 hunt_ep2.py "$@" >> batch3.log 2>&1; }
runs 301 6000 flat:6x6 0,1,2 5 s1
runs 302 6000 cyl:7x6 0,1,2 5 s2
runs 303 6000 flat:7x6 2,3,4 5 s3
runa 311 1500 cyl:7x6 0,1,2 4 3 0.5 y1
runa 312 1500 flat:6x6 0,1,2 4 3 0.5 y2
runa 313 1500 cyl:7x5 0,1,2 4 3 0.5 y3
rune 321 4000 cyl:7x6 0 5 e1
rune 322 4000 flat:7x6 2 5 e2
rune 323 4000 cyl:8x6 0,1,2,3 5 e3
echo done > batch3.done
