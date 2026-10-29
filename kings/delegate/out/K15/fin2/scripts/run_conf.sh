#!/bin/zsh
# P-model confirmation (kpp --pmodel, exact) of dud groups beside pawn contexts, all king states of the shuttle closure, both sides to move.
# chunks of 480 positions, each under a 58 CPU-second limit (no lock needed), nice 15.
# usage: run_conf.sh <tag> <board> <groupfile> <nctx> [ztype=dud]
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/fin2
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
tag=$1; board=$2; gf=$3; nctx=$4; z=${5:-dud}
extra=--allstates; [[ $z != dud ]] && extra=""
$PY conf2.py gen $board $z $gf cf/$tag --nctx $nctx --seed 11 $extra > cf/$tag.gen.log
rm -f cf/$tag.chunk.* cf/$tag.out; split -l 480 cf/$tag.in cf/$tag.chunk.
for c in cf/$tag.chunk.??; do
  [[ -f $c.out ]] && continue
  ( ulimit -t 58; nice -n 15 ./bin/kpp --board $board --ep on --cap 0 --pmodel < $c > $c.out 2> /dev/null )
  echo "$c $(wc -l < $c.out)/$(wc -l < $c)" >> cf/$tag.progress
done
cat cf/$tag.chunk.??.out > cf/$tag.out
$PY conf2.py cmp cf/$tag cf/$tag.out > cf/$tag.cmp.txt
echo finished >> cf/$tag.progress
