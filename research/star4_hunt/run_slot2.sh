#!/bin/bash
cd "$(dirname "$0")"
H=./h4
ext() { # name kind width seedfile k extra...
  local name=$1 kind=$2 width=$3 seeds=$4 k=$5; shift 5
  [ -f logs/$name.done ] && return
  nice -n 15 $H --$kind --width $width --single --max-entries 16777216 --evalbudget 5000000 --extend $seeds --k $k --rep-nim 3 --rep-m 99 --near 3 "$@" > out/$name.out 2> logs/$name.err && touch logs/$name.done
}
ext j4_c7star3_to_c8 cylinder 8 seeds/c7_reps.txt 6 --rot 7 --newonly
ext j1a_A_w6_k6 flat 6 seeds/A.txt 6 --newonly
ext j2_cores2_w6_k4 flat 6 seeds/cores2_all.txt 4 --newonly
ext j3_cores3_w7_k3 flat 7 seeds/cores3_all.txt 3 --newonly
ext j1b_A_w7_k4 flat 7 seeds/A.txt 4 --newonly
echo ALLDONE > logs/slot2.done
