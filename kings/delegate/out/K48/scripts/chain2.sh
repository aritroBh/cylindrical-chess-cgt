#!/bin/zsh
# K48 restart after the 12:13 reboot. chain2.sh IMPL "W:t1 t2 ..." "W:..." ... : each argument is one heavy.sh batch (scripts/batch_flat.sh);
# before each batch wait until the 5-minute load average is under 12.
cd "$(dirname $0)/.."
impl=$1; shift
for b in "$@"; do
  W=${b%%:*}; ts=(${=b#*:})
  until (( $(sysctl -n vm.loadavg | awk '{print int($3)}') < 12 )); do sleep 30; done
  echo "$$ batch2 $impl W=$W ${ts[*]} $(date +%H:%M:%S)" >> pids.log
  ../../heavy.sh scripts/batch_flat.sh $impl $W $ts
  sleep 20
done
echo done > logs/chain2_$impl.done
