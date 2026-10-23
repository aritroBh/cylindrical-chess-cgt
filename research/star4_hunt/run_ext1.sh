#!/bin/bash
# extension K=3 runs from *3 representatives; one process
cd "$(dirname "$0")"
run() { # name width seeds k extra
  nice -n 15 ./h4 --flat --width $2 --single --max-entries 33554432 --extend $3 --k $4 --rep-nim 3 --rep-m 99 $5 > out/ext_$1.out 2> logs/ext_$1.err
}
run w5reps_w5_k3 5 seeds/w5_reps.txt 3
run w4rep_w4_k3 4 seeds/w4_reps.txt 3
run w4rep_w5_k3 5 seeds/w4_reps.txt 3
run w4rep_w6_k3 6 seeds/w4_reps.txt 3
run w5reps_w6_k3 6 seeds/w5_reps.txt 3
run w6reps_w6_k3 6 seeds/w6_reps.txt 3
echo DONE > logs/ext1.done
