#!/bin/zsh
# suite_D.sh : (a) kq3 at cap 2, both bounds, on the four 3-pawn positions behind rows 1-4; (b) ownref (K27 referee's ownchess + the capture
# refinement) at cap 1 on the five children, both bounds, refine off / on; (c) kp28 (kpsolve + per-colour caps / promotion sets, an 84-line
# patch) on the row-5 child with White restricted to one queen (bound B' <= true), cap 2; (d) kq3 vs kp28 on the restricted mode, 28 cap-2
# positions; (e) kq3 at full cap 2 on the row-5 child (memory estimate close to the 3 GB limit; the watchdog guards it).
# ONE heavy.sh job, every solver under watch2.sh.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K28
cd $D; mkdir -p logs/D
step() {  # step NAME IN WALL CMD...
  n=$1; in=$2; w=$3; shift 3
  # guard: never more than 2 of my solver processes at once (the shared lock has been seen to lose a slot under load)
  while [ $(ps -eo command | grep -cE '^bin/(kq3|kp|kp28|ownref|ownchess) ') -ge 2 ]; do sleep 20; done
  echo "$$ suite_D $n $(date +%H:%M:%S)" >> $D/pids.log
  zsh $D/scripts/watch2.sh $D/logs/D/$n.pid 3000000 $w "$@" < $in > $D/logs/D/$n.out 2> $D/logs/D/$n.err
}
step F4_kq3_cap2      logs/rowsF.in     5400 bin/kq3 --cap 2 --bound AB --moves --threads 3
for r in 0 1; do for b in 0 1; do
step c5_own_b${b}_r${r} logs/children5.in 3000 bin/ownref 7 6 $b $r
done; done
step R5_kp28_B_w1Q    logs/r5.in        5400 bin/kp28 --board flat:7x6 --ep on --promote QRBN --promw Q --capw 1 --cap 2 --threads 3 --moves
step R5_kids_kq3_B_w1Q logs/r5kids.in 5400 bin/kq3 --cap 2 --capw 1 --promw Q --bound B --moves --threads 3
step V_kp28_w1Q       logs/test_exact2.in 5400 bin/kp28 --board flat:7x6 --ep on --promote QRBN --promw Q --capw 1 --cap 2 --moves
step V_kq3_w1Q        logs/test_exact2.in 5400 bin/kq3 --cap 2 --capw 1 --promw Q --bound AB --moves --threads 3
step R5_kq3_cap2      logs/r5.in        5400 bin/kq3 --cap 2 --bound AB --moves --threads 3
echo done > $D/logs/D/suite.done
