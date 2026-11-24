#!/bin/zsh
# K55 part 1, cyl:10x6 group G10: both solvers were stopped by the 2.9 GB cap after 44 (za) and 34 (rz) tests, because
# their memory grew from test to test.  The remaining tests run in chunks of 5, one fresh process per chunk.
# za now also frees its node list after the build; a short regression on cyl:8x6 first.
cd "$(dirname $0)"
echo "$$ run_p1g10.sh $(date)" >> pids.log
./capped.sh logs/p1_za_G8reg2.out logs/p1_za_G8reg2.err src/za_k55 8 6 ../K47/roots8.txt tests_ref27.txt N
for f in chunks/za_*.txt; do b=${f:t:r}
  ./capped.sh logs/g10/$b.out logs/g10/$b.err src/za_k55 10 6 roots_G10.txt $f N; done
for f in chunks/rz_*.txt; do b=${f:t:r}
  ./capped.sh logs/g10/$b.out logs/g10/$b.err src/rz_k55 10 6 roots_G10.txt $f N; done
echo done > logs/p1g10.done
