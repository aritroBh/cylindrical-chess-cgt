#!/bin/zsh
# K48: wait for the orphaned A job (files 1,3,4 on flat 8x6; its driver was stopped) to end, mark it done, then restart the A queue.
cd "$(dirname $0)/.."
while ps -p $1 >/dev/null 2>&1; do sleep 10; done
echo "rc=orphan $(date +%H:%M:%S)" > logs/flat/A_flat8x6_f1_3_4.done
sleep 20
exec scripts/queue_flat.sh A 8 9 10
