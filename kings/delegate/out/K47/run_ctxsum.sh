#!/bin/zsh
# K47 item 3: D-sum r(Z_O + C) for the cyl:9x6 contexts (C = the context pawns as a D-game), implementation A
cd "$(dirname $0)"
./za_k47 9 6 roots8.txt ctx_c9h.tg N > logs/ctxsum_c9h_A.out 2> logs/ctxsum_c9h_A.err
echo done > logs/ctxsum.done
