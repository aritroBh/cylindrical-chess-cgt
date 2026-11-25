#!/bin/zsh
# K63 question 3, 2 + 2 contexts on files g, h: the positions in chunks (a fresh solver process per chunk keeps the
# layer memo small), ref3m and kp_p --pmodel on each. usage: src/run_ctx_chunks.sh <tag>
cd "$(dirname $0)/.."
tag=$1; mkdir -p logs/${tag}_chunks
for c in in/${tag}_chunks/c*; do
  b=${c:t}
  zsh src/hrun.sh ${tag}_chunks/${b}_ref3m $c bin/ref3m --board pln:8x8
  zsh src/hrun.sh ${tag}_chunks/${b}_kpp $c bin/kp_p10 --board flat:8x8 --pmodel --cap 1 --threads 1
done
cat logs/${tag}_chunks/c*_ref3m.out > logs/ctx_${tag}_ref3m.out
cat logs/${tag}_chunks/c*_kpp.out > logs/ctx_${tag}_kpp.out
echo done > logs/ctx_$tag.done
