#!/bin/zsh
# K47 item 3: D-sum r(Z_O + C) for the sampled cyl:10x6 contexts, implementation A
cd "$(dirname $0)"
./za_k47 10 6 roots8.txt ctx_c10s.tg N > logs/ctxsum_c10s_A.out 2> logs/ctxsum_c10s_A.err
echo done > logs/ctxsum10.done
