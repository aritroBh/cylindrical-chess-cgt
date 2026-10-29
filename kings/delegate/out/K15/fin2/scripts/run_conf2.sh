#!/bin/zsh
# P-model confirmation (kpp --pmodel, exact), restartable: gen once, then chunks of CH positions (default 480), each under a 58 CPU-second limit
# (no lock, nice 15).  A chunk that does not finish is split in four and retried (down to 8 positions); positions still unfinished are reported as missing.
# usage: run_conf2.sh <tag> <board> <groupfile> <nctx> <ztype> [chunk=480]
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
tag=$1; board=$2; gf=$3; nctx=$4; z=$5; CH=${6:-480}
extra=--allstates; [[ $z != dud ]] && extra=""
if [[ ! -s cf/$tag.in || ! -s cf/$tag.rows.json ]]; then
  $PY conf2.py gen $board $z $gf cf/$tag --nctx $nctx --seed 11 $extra > cf/$tag.gen.log
  rm -f cf/$tag.chunk.* cf/$tag.out; split -l $CH cf/$tag.in cf/$tag.chunk.
fi
runchunk() { local c=$1; local n=$(wc -l < $c); local m=0
  [[ -f $c.out ]] && m=$(wc -l < $c.out)
  (( m == n )) && return
  ( ulimit -t 58; nice -n 15 ./bin/kpp --board $board --ep on --cap 0 --pmodel < $c > $c.out 2> /dev/null )
  m=$(wc -l < $c.out)
  if (( m < n )); then
    if (( n > 8 )); then
      rm -f $c.out $c.s.*; split -l $(( (n + 3) / 4 )) $c $c.s.
      for s in $c.s.??; do runchunk $s; done
      cat $c.s.??.out > $c.out
    else echo "$c unfinished $m/$n" >> cf/$tag.progress; fi
  fi }
for c in cf/$tag.chunk.??; do runchunk $c; echo "$c $(wc -l < $c.out)/$(wc -l < $c)" >> cf/$tag.progress; done
cat cf/$tag.chunk.??.out > cf/$tag.out
$PY conf2.py cmp cf/$tag cf/$tag.out > cf/$tag.cmp.txt
echo finished >> cf/$tag.progress
