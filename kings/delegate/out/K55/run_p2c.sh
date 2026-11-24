#!/bin/zsh
# K55 part 2: Z_O (cyl:8x6) against tests55c.txt (the loopy candidates and their negatives), both solvers, one process per test
cd "$(dirname $0)"
echo "$$ run_p2c.sh $(date)" >> pids.log
for f in chunks55c/t*.txt; do b=${f:t:r}
  ./capped.sh logs/p2c/za_$b.out logs/p2c/za_$b.err src/za_k55 8 6 roots_G8.txt $f N
  ./capped.sh logs/p2c/rz_$b.out logs/p2c/rz_$b.err src/rz_k55 8 6 roots_G8.txt $f N
done
echo done > logs/p2c.done
