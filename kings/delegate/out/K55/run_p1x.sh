#!/bin/zsh
# K55 part 1 extra: the 2 + 3 group of cyl:10x6 (equal to over on the 275 tests) against the enlarged batteries too
cd "$(dirname $0)"
echo "$$ run_p1x.sh $(date)" >> pids.log
for t in tests55 tests55b; do
  ./capped.sh logs/p1x_za_H10_$t.out logs/p1x_za_H10_$t.err src/za_k55 10 6 roots_H10.txt $t.txt N
  ./capped.sh logs/p1x_rz_H10_$t.out logs/p1x_rz_H10_$t.err src/rz_k55 10 6 roots_H10.txt $t.txt N
done
echo done > logs/p1x.done
