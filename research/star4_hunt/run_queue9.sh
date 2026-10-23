#!/bin/bash
# rows of facing pairs (gap 1) plus up to K extra pawns anywhere on the same files; then new-file extensions of cores
cd "$(dirname "$0")"
while [ ! -f logs/r3_prim_c7_k3.done ]; do sleep 15; done
x() { # name width seeds k extra...
  local name=$1 w=$2 seeds=$3 k=$4; shift 4
  [ -f logs/$name.done ] && return
  nice -n 15 ./h4 --flat --width $w --single --max-entries 16777216 --evalbudget 500000 --extend $seeds --k $k --rep-nim 3 --rep-m 99 --near 3 "$@" > out/$name.out 2> logs/$name.err && touch logs/$name.done
}
x j3_cores3_w7_k3 7 seeds/cores3_all.txt 3 --newonly
x rows_w4_k3 4 seeds/rows_w4.txt 3
x j2_cores2_w6_k3 6 seeds/cores2_all.txt 3 --newonly
x rows_w5_k2 5 seeds/rows_w5.txt 2
x j1a_A_w6_k5 6 seeds/A.txt 5 --newonly
echo ALLDONE > logs/queue9.done
