#!/bin/zsh
# referee queue 3: starts when queue 1 has finished (keeps at most 2 referee jobs at once)
while [[ ! -f queue1.done ]]; do sleep 30; done
../../../heavy.sh ./r45b val cyl:10x6 < ../ctx_positions.txt > ctx_r45.out 2> ctx_r45.err
for w in 10 11 12; do ../../../heavy.sh ./r45b layers cyl:${w}x6 < battery_layers.txt > battery_W$w.out 2> battery_W$w.err; done
for fs in 0,1,3 0,1,4 0,1,5 0,2,4 0,2,5; do ../../../heavy.sh ./r45b enum cyl:6x6 $fs 3 3 > enum_6_${fs//,/}.out 2> enum_6_${fs//,/}.err; done
echo done > queue3.done
