#!/bin/bash
# ring experiments with ring4 (width up to 10); runs after slot2b
cd "$(dirname "$0")"
while [ ! -f logs/slot2b.done ]; do sleep 15; done
r4() { # name width seeds k extra...
  local name=$1 w=$2 seeds=$3 k=$4; shift 4
  [ -f logs/$name.done ] && return
  nice -n 15 ./ring4 --cylinder --width $w --single --max-entries 16777216 --evalbudget 4000000 --extend $seeds --k $k --rot 7 --newonly --rep-nim 3 --near 3 "$@" > out/$name.out 2> logs/$name.err && touch logs/$name.done
}
r4 r1_prim_c8_k5 8 seeds/c7_prim.txt 5
r4 r1_prim_c9_k3 9 seeds/c7_prim.txt 3
r4 r1_all_c8_k4 8 seeds/c7_reps.txt 4
r4 r1_all_c9_k3 9 seeds/c7_reps.txt 3
echo ALLDONE > logs/queue3.done
