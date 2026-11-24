#!/bin/zsh
# K48 part 3: files a, b, e on cyl:8x7, <= 3 + 3 pawns (ranks 2..6), every king placement; A = p45a (both orientations), R = r48 enum (under).
cd "$(dirname $0)/.."
until (( $(sysctl -n vm.loadavg | awk '{print int($3)}') < 12 )); do sleep 30; done
echo "$$ tall A cyl8x7 $(date +%H:%M:%S)" >> pids.log
../../heavy.sh bin/p45a --kind cyl --W 8 --H 7 --files 0,1,4 --nw 3 --nb 3 --mode both > logs/tall/A_cyl8x7_f0_1_4.out 2> logs/tall/A_cyl8x7_f0_1_4.err
echo "rc=$? $(date +%H:%M:%S)" > logs/tall/A_cyl8x7_f0_1_4.done
sleep 20
until (( $(sysctl -n vm.loadavg | awk '{print int($3)}') < 12 )); do sleep 30; done
echo "$$ tall R cyl8x7 $(date +%H:%M:%S)" >> pids.log
../../heavy.sh bin/r48 enum cyl:8x7 0,1,4 3 3 > logs/tall/R_cyl8x7_f0_1_4.out 2> logs/tall/R_cyl8x7_f0_1_4.err
echo "rc=$? $(date +%H:%M:%S)" > logs/tall/R_cyl8x7_f0_1_4.done
