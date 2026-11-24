#!/bin/zsh
# K55 part 2: Z_O (cyl:8x6) against the supplementary battery tests55b.txt, convention N, both solvers.
# The first attempt (one process for all tests, games up to 120 nodes) passed the 2.9 GB cap and was stopped; the games
# were made smaller (tiny-13 instead of tiny-20 in the sums) and every test now runs in a fresh process.
cd "$(dirname $0)"
echo "$$ run_p2b.sh $(date)" >> pids.log
for f in chunks55b/t*.txt; do b=${f:t:r}
  ./capped.sh logs/p2b/za_$b.out logs/p2b/za_$b.err src/za_k55 8 6 roots_G8.txt $f N
  ./capped.sh logs/p2b/rz_$b.out logs/p2b/rz_$b.err src/rz_k55 8 6 roots_G8.txt $f N
done
echo done > logs/p2b.done
