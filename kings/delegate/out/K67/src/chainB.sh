#!/bin/zsh
# K67 phase C: r48 (under orientation) on the two new classes, the two runs side by side (each through src/run.sh:
# heavy.sh queue, /usr/bin/time -l, watchdog).  Not started if logs/STOP exists.
cd "$(dirname $0)/.."
[[ -f logs/STOP ]] && { echo "STOP present"; exit 1; }
zsh src/run.sh search/R88_f0_1_4 bin/r48 enum flat:8x8 0,1,4 3 3 &
sleep 20
zsh src/run.sh search/R88_f0_3_4 bin/r48 enum flat:8x8 0,3,4 3 3 &
wait
for t in R88_f0_1_4 R88_f0_3_4; do echo "$t $(cat logs/search/$t.rc) $(grep ' real' logs/search/$t.err) $(grep 'maximum resident' logs/search/$t.err)"; done
echo "chain B done $(date +%H:%M:%S)"
