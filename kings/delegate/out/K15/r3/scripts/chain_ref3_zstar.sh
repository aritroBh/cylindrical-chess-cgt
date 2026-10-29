#!/bin/zsh
# K15 r3: ref3 (independent P solver) on 16 sampled Z* context positions (<= 2 context pawns, file g), one position per run, ulimit -t 58, after the survivor chain
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K15/r3
while [[ ! -f logs/surv_chain.done ]]; do sleep 15; done
: > data/zstar_ref16.out
while read -r l; do
  ( ulimit -t 58; echo "$l" | nice -n 15 bin/ref3 --board cyl:8x6 2>/dev/null ) | grep ' | ' >> data/zstar_ref16.out || true
done < data/zstar_ref16.in
echo finished > logs/ref3_zstar.done
