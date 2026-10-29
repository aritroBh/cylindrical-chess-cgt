#!/bin/zsh
# suite_E.sh : my own re-run of kpsolve at cap 2 on the four 3-pawn positions behind rows 1-4 (the earlier attempt's logs/r/cap2_F1.out and
# cap2_F2.out came from a byte-identical build; this re-run is for provenance).  One run, both bounds, with move values.
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K28
cd $D; mkdir -p logs/E
step() {
  n=$1; in=$2; w=$3; shift 3
  while [ $(ps -eo command | grep -cE '^bin/(kq3|kp|kp28|ownref|ownchess) ') -ge 2 ]; do sleep 20; done
  echo "$$ suite_E $n $(date +%H:%M:%S)" >> $D/pids.log
  zsh $D/scripts/watch2.sh $D/logs/E/$n.pid 3000000 $w "$@" < $in > $D/logs/E/$n.out 2> $D/logs/E/$n.err
}
step F4_kp_cap2 logs/rowsF.in 5400 bin/kp --board flat:7x6 --ep on --promote QRBN --cap 2 --threads 2 --moves
echo done > $D/logs/E/suite.done
