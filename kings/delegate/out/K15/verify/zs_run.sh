#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/verify
for f in $(ls zs | grep -v '\.out$'); do
  n=$(wc -l < zs/$f)
  if [ -s zs/$f.out ] && [ $(wc -l < zs/$f.out) -ge $n ]; then continue; fi
  ( ulimit -t 100; nice -n 15 bin/ref3 --board cyl:8x6 < zs/$f > zs/$f.out 2> zs/$f.err )
  echo "$f $(wc -l < zs/$f.out)/$n" >> logs/zs_run.log
done
echo finished >> logs/zs_run.log
