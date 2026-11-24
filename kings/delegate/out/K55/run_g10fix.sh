#!/bin/zsh
# K55 part 1, G10: the tests that the 2.9 GB cap cut off in the chunked runs, one fresh process per test
cd "$(dirname $0)"
echo "$$ run_g10fix.sh $(date)" >> pids.log
mkdir -p logs/g10fix
for f in chunks_g10fix/*.txt; do b=${f:t:r}; s=${b%%_*}
  ./capped.sh logs/g10fix/$b.out logs/g10fix/$b.err src/${s}_k55 10 6 roots_G10.txt $f N; done
echo done > logs/g10fix.done
