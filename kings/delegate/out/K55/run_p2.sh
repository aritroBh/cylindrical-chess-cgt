#!/bin/zsh
# K55 part 2: Z_O (cyl:8x6) against the enlarged battery (tests55.txt), convention N, both solvers; then the stopper test
cd "$(dirname $0)"
echo "$$ run_p2.sh $(date)" >> pids.log
./capped.sh logs/p2_za_G8.out logs/p2_za_G8.err src/za_k55 8 6 roots_G8.txt tests55.txt N
./capped.sh logs/p2_rz_G8.out logs/p2_rz_G8.err src/rz_k55 8 6 roots_G8.txt tests55.txt N
for g in G8:8 G9:9 G10:10 H10:10; do n=${g%%:*}; w=${g##*:}
  ./capped.sh logs/stop_$n.out logs/stop_$n.err src/rz_k55 $w 6 roots_$n.txt t0.txt N stopper
done
echo done > logs/p2.done
