#!/bin/zsh
# K59 part 1c: T3 (pr56: 14.3 million nodes) with vgsum59 --lowmem and a capacity hint, under the RSS watchdog.
cd "$(dirname $0)/.."
../../heavy.sh /usr/bin/time -l bin/vgsum59 --lowmem --reserve 17500000 0 --board cyl:8x7 --root "Kd4 kf4 Pb3 Pb5 Pe2 pa5 pb6 pe6" --shuttle f5 > logs/p1_T3.out 2> logs/p1_T3.err &
P=$!; echo "$P heavy.sh p1_T3 $(date +%H:%M:%S)" >> pids.log
src/watch.sh $P p1_T3 &
W=$!; echo "$W watch.sh p1_T3" >> pids.log
wait $P; wait $W
