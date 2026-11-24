#!/bin/zsh
# K48 referee, claim 1: d4 root (White to move) and its q (both sides to move) of Z_O in chess on cyl:8x6, cap 1,
# with fresh builds of own39 (both bounds, refinement on) and kpsolve (both bounds, no refinement). Run from verify/.
cd "$(dirname $0)/.."
H=../../../heavy.sh
run() { name=$1; in=$2; shift 2
  $H /usr/bin/time -l "$@" < $in > logs/$name.out 2> logs/$name.err &
  echo "$! heavy.sh $name" >> pids.log; wait $!; echo "done $(date +%H:%M:%S)" >> logs/$name.out.done; }
run own39_B_root in/root_d4w.in bin/own39 8 6 1 1 1 1
run own39_A_d4q in/d4_q.in bin/own39 8 6 1 0 1 1
run own39_B_d4q in/d4_q.in bin/own39 8 6 1 1 1 1
run kpsolve_d4q in/d4_q.in bin/kpsolve --board cyl:8x6 --ep on --promote QRBN --cap 1 --moves
echo done > logs/chess.done
