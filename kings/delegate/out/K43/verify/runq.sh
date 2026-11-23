#!/bin/zsh
# referee queue: one heavy process at a time through heavy.sh (nice 15)
cd "$(dirname "$0")"
HV=../../../heavy.sh
echo "queue $$" >> pids.log
for spec in "cyl:7x6 0-2 20" "cyl:6x6 0-3 0" "cyl:7x6 0-3 0" "flat:7x6 0-3 0" "flat:7x6 1-4 0" "cyl:8x6 0-3 0" "flat:8x6 0-3 0" "flat:8x6 1-4 0" "flat:8x6 2-5 0" "cyl:9x6 0-3 0"; do
  set -- ${=spec}
  tag=${1/:/}_$2
  [[ -f logs/$tag.done ]] && continue
  /usr/bin/time -l $HV ./rv43 --board $1 --files $2 --maxw 3 --maxb 3 --list $3 > logs/$tag.out 2> logs/$tag.err &
  echo "$tag $!" >> pids.log
  wait $!
  touch logs/$tag.done
done
echo done > logs/queue.done
