#!/bin/zsh
# K63: process the given chunks of a context tag with ref3m and kp_p (skips chunks whose outputs are complete).
# usage: src/run_chunks2.sh <tag> <chunk>...   e.g. gh22 c03 c04
cd "$(dirname $0)/.."
tag=$1; shift
for b in "$@"; do
  c=in/${tag}_chunks/$b
  grep -q "maximum res" logs/${tag}_chunks/${b}_ref3m.err 2>/dev/null || zsh src/hrun.sh ${tag}_chunks/${b}_ref3m $c bin/ref3m --board pln:8x8
  grep -q "maximum res" logs/${tag}_chunks/${b}_kpp.err 2>/dev/null || zsh src/hrun.sh ${tag}_chunks/${b}_kpp $c bin/kp_p10 --board flat:8x8 --pmodel --cap 1 --threads 1
done
echo done > logs/chunks2_$1.done
