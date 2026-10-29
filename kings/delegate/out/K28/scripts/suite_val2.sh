#!/bin/zsh
# suite_val2.sh : cap-2 validation of kq3 against kpsolve on logs/test_exact2.in (28 positions, exact at cap 2 or not), ONE heavy.sh job.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K28
cd $D; mkdir -p logs/val
IN=logs/test_exact2.in
step() {
  n=$1; shift
  echo "$$ suite_val2 $n $(date +%H:%M:%S)" >> $D/pids.log
  zsh $D/scripts/watch2.sh $D/logs/val/$n.pid 3000000 2400 "$@" < $IN > $D/logs/val/$n.out 2> $D/logs/val/$n.err
}
step kp_cap2      bin/kp --board flat:7x6 --ep on --promote QRBN --cap 2 --moves
step kq3_cap2     bin/kq3 --cap 2 --bound AB --moves --threads 1
step kq3_cap2_ref bin/kq3 --cap 2 --bound AB --refine --moves --threads 1
echo done > $D/logs/val/suite2.done
