#!/bin/zsh
# All-promotions (QRBN) reruns of the 1/8 decisive end positions, for a full-chess certificate (open problem 1).
# Order: 8-man cap 1 (4 positions), then the cap-2 side (1 position). The 9-man set (26 GB-class) waits for memory.
# nice 15, 4 threads. The kpsolve PID of the current job is written to qrbn_current.pid.
cd "${0:A:h}/../.."
O=realchess/targets18
for job in "8man 1 kp_eighth_8man" "cap2 2 kp_eighth_cap2"; do
  set -- ${=job}
  [[ -s $O/qrbn_$1.out ]] && continue
  start=$(date +%s)
  nice -n 15 ./kings/kpsolve --board flat:8x8 --ep on --promote QRBN --cap $2 --threads 4 < $O/$3.txt > $O/qrbn_$1.out.tmp 2> $O/qrbn_$1.err &
  echo $! > $O/qrbn_current.pid; wait $!; rc=$?
  [[ $rc == 0 ]] && mv $O/qrbn_$1.out.tmp $O/qrbn_$1.out
  echo "exit $rc after $(( $(date +%s) - start )) s at $(date)" >> $O/qrbn_$1.err
done
