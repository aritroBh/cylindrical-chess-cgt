#!/bin/sh
cd "$(dirname "$0")"
d() { nice -n 10 python3 depth_check.py "$@" 2>&1 | tail -3; }
d rows_a1.json cyl:7x6 0,1,2 2500
d rows_a2.json cyl:7x6 1,2,3 2500
d rows_a3.json cyl:7x6 0,1 2500
d rows_a4.json cyl:7x6 0,1,2,3 2500
d rows_a5.json cyl:7x5 0,1,2 2500
d rows_a6.json flat:6x6 0,1,2 2500
d rows_a7.json flat:6x6 1,2 2500
d rows_a8.json flat:7x6 2,3,4 2500
d rows_a9.json cyl:6x6 0,1 2500
d rows_b2.json cyl:7x6 1,2,3 2500
d rows_b3.json flat:6x6 0,1,2 2500
d rows_e1.json cyl:7x6 0 2500
d rows_e2.json flat:7x6 2 2500
d rows_e3.json cyl:8x6 0,1,2,3 2500
d rows_c5.json cyl:7x5 0,1,2 2500
d rows_c6.json cyl:7x7 0,1,2 2500
d rows_c7.json cyl:8x6 0,1,2 2500
d rows_c8.json cyl:6x6 0,1 2500
