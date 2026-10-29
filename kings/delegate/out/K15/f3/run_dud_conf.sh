#!/bin/zsh
# regenerate (corrected group-file span) and run the P-model confirmation of all dud groups on cyl:7x6 and cyl:8x6, in chunks under 58 CPU-seconds
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/f3
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
for B in 7 8; do
  $PY conf2.py gen cyl:${B}x6 dud cf/g${B}x6_dud.txt cf/e${B}x6 --nctx 40 --seed 11 --allstates > cf/e${B}x6.gen.log
  rm -f cf/e${B}x6.chunk.* cf/e${B}x6.out; split -l 480 cf/e${B}x6.in cf/e${B}x6.chunk.
  for c in cf/e${B}x6.chunk.??; do
    ( ulimit -t 58; nice -n 15 ./kpp --board cyl:${B}x6 --ep on --cap 0 --pmodel < $c > $c.out 2> /dev/null )
    echo "$c $(wc -l < $c.out)/$(wc -l < $c)" >> cf/e.progress
  done
  cat cf/e${B}x6.chunk.??.out > cf/e${B}x6.out
  $PY conf2.py cmp cf/e${B}x6 cf/e${B}x6.out > cf/e${B}x6.cmp.txt
done
echo finished >> cf/e.progress
