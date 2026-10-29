#!/bin/zsh
# suite_val.sh : cap-1 validation suite + the cap-1 runs on the five children, run as ONE heavy.sh job (hrun.sh).  Every solver runs under
# watch2.sh (3 GB RSS, wall limit), one after the other.  Inputs: logs/test_cap1.in (120 positions, made by mk_tests.sh) and
# logs/children5.in (the five children of the brief).  Outputs: logs/val/*.out / *.err.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K28
cd $D; mkdir -p logs/val
step() {  # step NAME IN CMD...
  n=$1; in=$2; shift 2
  echo "$$ suite_val $n $(date +%H:%M:%S)" >> $D/pids.log
  zsh $D/scripts/watch2.sh $D/logs/val/$n.pid 3000000 1500 "$@" < $in > $D/logs/val/$n.out 2> $D/logs/val/$n.err
}
T=logs/test_cap1.in; C=logs/children5.in
step c5_kp_cap1      $C bin/kp --board flat:7x6 --ep on --promote QRBN --cap 1 --moves
step c5_kq3_cap1     $C bin/kq3 --cap 1 --bound AB --moves --threads 1
step c5_kq3_cap1_ref $C bin/kq3 --cap 1 --bound AB --refine --moves --threads 1
step kp_cap1      $T bin/kp --board flat:7x6 --ep on --promote QRBN --cap 1 --moves
step kq3_cap1     $T bin/kq3 --cap 1 --bound AB --moves --threads 1
step kq3_cap1_ref $T bin/kq3 --cap 1 --bound AB --refine --moves --threads 1
step own_A0       $T bin/ownref 7 6 0 0
step own_B0       $T bin/ownref 7 6 1 0
step own_A1       $T bin/ownref 7 6 0 1
step own_B1       $T bin/ownref 7 6 1 1
echo done > $D/logs/val/suite.done
