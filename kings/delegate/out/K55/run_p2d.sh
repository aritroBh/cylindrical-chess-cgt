#!/bin/zsh
# K55 part 2: Z_O (cyl:8x6) against tests55d.txt (the D-game candidates with a terminal and their negatives), both solvers, one process per test
cd "$(dirname $0)"
echo "$$ run_p2d.sh $(date)" >> pids.log
for f in chunks55d/t*.txt; do b=${f:t:r}
  ./capped.sh logs/p2d/za_$b.out logs/p2d/za_$b.err src/za_k55 8 6 roots_G8.txt $f N
  ./capped.sh logs/p2d/rz_$b.out logs/p2d/rz_$b.err src/rz_k55 8 6 roots_G8.txt $f N
done
echo done > logs/p2d.done
