#!/bin/zsh
# K63 question 3: P values of F2 + context (one board, one game), two solvers. usage: src/run_ctx.sh <tag>...
cd "$(dirname $0)/.."
for tag in "$@"; do
  zsh src/hrun.sh ctx_${tag}_ref3m in/ctx_$tag.pos bin/ref3m --board pln:8x8
  zsh src/hrun.sh ctx_${tag}_kpp in/ctx_$tag.pos bin/kp_p10 --board flat:8x8 --pmodel --cap 1 --threads 1
done
echo done > logs/ctx_$1.done
