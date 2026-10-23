#!/bin/bash
# extension of the two primitive C7 *3 rings by up to 3 extra pawns anywhere on the ring (11-13 pawns)
cd "$(dirname "$0")"
nice -n 15 ./ring4 --cylinder --width 7 --single --max-entries 16777216 --evalbudget 500000 --extend seeds/c7_prim.txt --k 2 --rep-nim 3 --near 3 > out/r3_prim_c7_k3.out 2> logs/r3_prim_c7_k3.err && touch logs/r3_prim_c7_k3.done
touch logs/queue3.done
