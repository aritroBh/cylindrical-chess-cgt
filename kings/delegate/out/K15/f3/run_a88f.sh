#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/f3/cf
rm -f a8x8f.progress
for c in a8x8f.chunk.??; do
  ( ulimit -t 58; nice -n 15 ../kpp --board cyl:8x8 --ep on --cap 0 --pmodel < $c > $c.out 2> /dev/null )
  echo "$c $(wc -l < $c.out)/$(wc -l < $c)" >> a8x8f.progress
done
cat a8x8f.chunk.??.out > a8x8f.out
PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames /Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python ../conf2.py cmp a8x8f a8x8f.out > a8x8f.cmp.txt
echo finished >> a8x8f.progress
